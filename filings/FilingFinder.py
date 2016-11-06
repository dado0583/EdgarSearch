'''
Created on Sep 18, 2016

@author: dave
'''


import sys
import os

try:
    sys.path.index(os.getcwd()) # Or os.getcwd() for this directory
except ValueError:
    sys.path.append(os.getcwd()) # Or os.getcwd() for this directory
     

from bson.binary import Binary
import concurrent.futures
import csv
import datetime
import logging
import re
import sys
import traceback
import urllib
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
import zlib

from bs4 import BeautifulSoup
from bs4.element import NavigableString

from ciks.CIKS import CIKS
from config.MongoDb import MongoDb
from config.Utils import getRaw
from config.Utils import getsoup
from sec_config.Coverage import SECCoverage

from sec_config.SearchTerms import SearchTerms
from filings.FilingSearcher import FilingSearcher


#from sec_coverage.Coverage import SECCoverage
class FilingFinder(object):
    domain = 'https://www.sec.gov'
    baseUrl = domain+ '/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=&dateb=&owner=exclude&start={}&count={}'    
        
    
    searchingTerms = SearchTerms().getSearchTerms()
    searcher = FilingSearcher(ciks=[], searchTerms=searchingTerms)
        
    def __init__(self, filingType="All", ciks=[]):
        self.filingType=filingType
        self.ciks=ciks

        #pool.submit(outputRaceResults, url)  
            
    def searchFilings(self):   
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:    
            for cik in self.ciks:
                pool.submit(self.searchFiling, cik)  
                        
    def getContents(self, rowData, header, cell):
        if "File/Film Number" in header:
            link = cell.find('a')
            if link is not None:
                rowData[header] =  link.text +'/'+ cell.find(text=True, recursive=False).rstrip()        
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

    def searchFiling(self, cik):
        print('Finding filings for CIK:{}'.format(str(cik)))
                
        try:
            count = 100
            filingsCollection = MongoDb().getDb('sec')['filings']
                    
            for page in range(1, 1000):
                soup = getsoup(FilingFinder.baseUrl.format(cik, count*page, count))
                table = soup.find('table', {"class":"tableFile2"})
                headers = []         
                
                companyName = "Unknown"
                
                try:
                    companyName = re.findall(r'.*(?=\sCIK)', soup.find('span', {"class":"companyName"}).text)[0]
                except:
                    pass
                                
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
                            
                        if (len(rowData)> 0 
                                and 'File/Film Number' in rowData
                                and self.filter(rowData["Filings"])):
                            
                            rowData["_id"] = rowData['File/Film Number']  
                            rowData["cik"] = cik    
                            rowData["companyName"] = companyName    
                            rowData["_timestamp"] = datetime.datetime.now()
    
                            if filingsCollection.find({'_id': rowData["_id"]},{"_id":1}).count() > 0:
                                continue
    
                            print('Found Filing {}, file number {} for {}/{}'.format(rowData["Filings"], rowData["_id"], companyName, cik))                                                                        
                            self.addInfo(rowData) 
                        
                            try:
                                print('{} Saving file for {}'.format(str(datetime.datetime.now()), rowData["_id"]))
                                filingsCollection.save(rowData)
                            except:
                                print('Cutting down file for {}'.format(rowData["_id"]))
                                filingsCollection.save(rowData)
                             
                            FilingFinder.searcher.searchFiling(cik, rowData)   
                    except Exception as e:
                        traceback.print_exc(file=sys.stdout)
                        logging.exception(e)
                        print(str(tr))
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            logging.exception(e)
            print(str(tr))
                 
    def addInfo(self, rowData):        
        if 'DocumentsLink' in rowData and rowData['DocumentsLink'] is not None:
            soup = getsoup(rowData['DocumentsLink'])
            urlForRawText = FilingFinder.domain + soup.find('a', text=re.compile("(.*)txt"))['href']
            rawText = getRaw(urlForRawText)
                
            compressedText = zlib.compress(rawText, 6)
            rowData['RawText'] = Binary(compressedText)
                
        if 'InteractiveData' in rowData and rowData['InteractiveData'] is not None:
            self.addInteractiveDataInfo(rowData)

    def addInteractiveDataInfo(self, rowData):
        soup = getsoup(rowData['InteractiveData'])
        
        #Note, that the reports can be .htm or .xml. Newer reports seem to be .htm so focusing on that first.
        scriptWithReportsLinks = soup.find('script', text=re.compile(".*InstanceReportXslt.*"))
        
        urls = []
        for line in scriptWithReportsLinks.text.splitlines():
            try:
                url = FilingFinder.domain + re.findall("/Archives.*[\.htm|\.xml]", line)[0]
                                
                if url.endswith(".htm") or url.endswith(".xml"):
                    urls.append(url)
            except:
                pass
        
        rowData['InteractiveDataUrl'] = urls
        
        reportsData= []
        for url in urls:
            soup = getsoup(url)
            reportsData.append({"url":url, "html": soup.html.encode("utf-8")})
                        
        rowData['InteractiveDataTables'] = reportsData 
          
    def filter(self, filings):
        if ("10-Q" in filings
                or "10-K" in filings):
            return True
        else:
            return False
        
if __name__ == "__main__":
    cik_codes = SECCoverage().getSearchTerms()
    FilingFinder(ciks=cik_codes).searchFilings()
            