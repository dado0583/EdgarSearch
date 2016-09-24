'''
Created on Sep 18, 2016

@author: dave
'''
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import csv
import datetime
import re
import urllib
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from ciks.CIKS import CIKS
from config.MongoDb import MongoDb
from htmlCache import Utils


class FilingFinder(object):
    domain = 'https://www.sec.gov'
    baseUrl = domain+ '/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=&dateb=&owner=exclude&start={}&count={}'    
        
    def __init__(self, filingType="All", ciks=[]):
        self.filingType=filingType
        self.ciks=ciks
            
    def findFilings(self):                
        for cik in self.ciks:
            self.findFiling(cik)
                        
    def getContents(self, rowData, header, cell):
        if "File/Film Number" in header:
            rowData[header] =  cell.find('a').text +'/'+ cell.find(text=True, recursive=False).rstrip()        
        elif "Format" in header:
            try:
                rowData['DocumentsLink'] = FilingFinder.domain + str(cell.find('a', {"id":"documentsbutton"})['href'])
            except:
                pass
                        
            try:
                rowData['InteractiveData'] = FilingFinder.domain + str(cell.find('a', {"id":"interactiveDataBtn"})['href'])
            except:
                pass
        else:    
            rowData[header] = str(cell.text).rstrip()

    def findFiling(self, cik):
        count = 100
        filingsCollection = MongoDb().getDb('sec')['filings']
                
        for page in range(1, 1000):
            soup = Utils.getsoup(FilingFinder.baseUrl.format(cik, count*page, count))
            table = soup.find('table', {"class":"tableFile2"})
            headers = []            
            
            if table is None:
                continue
            
            for tr in table.find_all("tr"):
                rowData = {}
                
                if len(headers) == 0:
                    for th in tr.find_all('th'):
                        headers.append(str(th.text).rstrip())
                
                tds = tr.find_all('td')
                
                try:
                    for i in range(0, len(tds)):
                        self.getContents(rowData, headers[i], tds[i])
                        
                    if len(rowData)> 0 and filingsCollection.find({"_id": rowData['File/Film Number']}).count() == 0: 
                        rowData["_id"] = rowData['File/Film Number']    
                        rowData["_timestamp"] = datetime.datetime.now()
                        self.addInfo(rowData)   
                        filingsCollection.save(rowData)
                    
                    if 'InteractiveData' in rowData and rowData['InteractiveData'] is not None:
                        self.addInteractiveDataInfo(rowData)
                except Exception as e:
                    print(e)
                    print(rowData)
                    print(str(tr))
                          
                        
    
    def addInfo(self, rowData):
        if 'DocumentsLink' in rowData and rowData['DocumentsLink'] is not None:
            soup = Utils.getsoup(rowData['DocumentsLink'])
            urlForRawText = FilingFinder.domain + soup.find('a', text=re.compile("(.*)txt"))['href']
            rawText = Utils.getRaw(urlForRawText)
            
            rowData['RawText'] = rawText
        
        if 'InteractiveData' in rowData and rowData['InteractiveData'] is not None:
            self.addInteractiveDataInfo(rowData)

    def addInteractiveDataInfo(self, rowData):
        soup = Utils.getsoup(rowData['InteractiveData'])
        
        reportNumbers = []
        
        try:
           pass
            #for tag in soup.select('ul li a.xbrlviewer'):
               # reportNumbers.append(int(re.findall(r'\\d+', tag['href'])[0])+1) ##Adding 1 because this is what SEC does
            #tables are stored in separate html urls. Need to deocompose the report numbers from the javascript funciton, then get the html manually
        except Exception as e:
            print(e)
            print(rowData)
            print(str(tr))
            
            #Note, that the reports can be .htm or .xml. Newer reports seem to be .htm so focusing on that first.
        scriptWithReportsLinks = soup.find('script', text=re.compile(".*InstanceReportXslt.*"))
        print(scriptWithReportsLinks.text)
        
        #split the line by line breaks and find lines that match the pattern, extracting urls
        
        split = scriptWithReportsLinks.text.split("\'all\'")
        re.findall(r'.*reports[\\d.*\\d].*;', scriptWithReportsLinks.text, re.DOTALL | re.MULTILINE)
        #Need to parse the javascript and grab the links to the reports
        #PARSE LOOKING FOR reports[%d+%d].... Then extract the link
        pass
        
FilingFinder(ciks=[51143]).findFilings()
            
            