'''
Created on Sep 18, 2016

@author: dave
'''
import os
import sys
import zlib
import random
import datetime
import re

try:
    sys.path.index(os.getcwd()) # Or os.getcwd() for this directory
except ValueError:
    sys.path.append(os.getcwd()) # Or os.getcwd() for this directory
     
import concurrent.futures     
from config.MongoDb import MongoDb
from config.MongoDb import Env
from sec_config.Coverage import SECCoverage
from sec_config.SearchTerms import SearchTerms

class FilingSearcher(object):
    domain = 'https://www.sec.gov'
    baseUrl = domain+ '/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=&dateb=&owner=exclude&start={}&count={}'    
        
    def __init__(self, filingType="All", ciks=[], searchTerms=[]):
        self.filingType=filingType
        self.ciks=ciks
        self.searchTerms=searchTerms

        #pool.submit(outputRaceResults, url)  
            
    def searchAllFilings(self):                   
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:  
            #pool.submit(self.searchFiling, self.searchTerms, 879101)
             
            #if True:
            #    return 
        
            random.shuffle(self.ciks)           
            for cik in self.ciks:
                pool.submit(self.searchFiling, self.searchTerms, cik) 

    def searchFiling(self, cik, item):
        searchCollection = MongoDb(Env.dev).getDb('sec')['searchresults']
            
        resultsData = {}
        resultsData["cik"] = cik
        resultsData["_id"] = item['_id']
        
        text = zlib.decompress(item['RawText']).decode("utf-8")
        matchFound = False
        matches = self.findMatches(text)
        
        if len(matches) > 0:
            print ("{} Matches for {} (ID={}) are {}".format(str(datetime.datetime.now()), cik, item['_id'], matches))
            resultsData["raw_matches"] = matches
            matchFound = True
            

                
        if 'InteractiveDataTables' in item and item['InteractiveDataTables'] is not None:
            tables = item['InteractiveDataTables']
            for table in tables:
                url = table["url"]
                text = str(table['html'])
                matches = {}
                
                for bucket in self.searchTerms:
                    for string in self.searchTerms[bucket]:
                        if string in text:
                            print ("Match found! {} in {}".format(string, text[:100]))
                            if bucket not in matches or len(matches[bucket]) == 0:
                                matches[bucket] = []
                            matches[bucket].append({string, text})
                
                if len(matches) > 0:
                    print ("{} Matches for {} (ID={}) are {}".format(str(datetime.datetime.now()), cik, item['_id'], matches.keys()))
                    resultsData["table_matches"] = matches
                    matchFound = True
        
        if matchFound:
            searchCollection.save(resultsData)

    def searchFilings(self, cik):
        try:
            print('{} Searching filings for CIK:{}'.format(str(datetime.datetime.now()), str(cik)))                
            filingsCollection = MongoDb().getDb('sec')['filings']
            
            collection = filingsCollection.find({"cik":cik})#{"_id": "001-36011/131050730"}, {"RawText":1, "InteractiveDataTables":1, "_id":1})
                        
            for item in collection:  
                self.searchFiling(cik, item)
                    
        except Exception as e:
            logging.exception(e)
            print(str(e))
  
    def findMatches(self, item):
        matches = {}
        
        lines = item.split('\n')
        
        prevLine = lines[0]
        currentLine = lines[1]
        nextLine = lines[2]
        
        for nextlineNum in range(3, len(lines)):
            #print(prevLine + currentLine + nextLine)
                
            for bucket in self.searchTerms:
                for string in self.searchTerms[bucket]:                    
                    if string in currentLine:
                        print("Match found! {} in {}".format(string, currentLine))
                        
                        if bucket not in matches or len(matches[bucket]) == 0:
                            matches[bucket] = []
                        
                        matches[bucket].append({
                            string, 
                            str(nextlineNum-2) +":"+ prevLine +os.linesep+
                            str(nextlineNum-1) +":"+ currentLine +os.linesep+
                            str(nextlineNum) +":"+ nextLine})

            prevLine = lines[nextlineNum-2]
            currentLine = lines[nextlineNum-1]
            nextLine = lines[nextlineNum]
                            
        return matches
            
if __name__ == "__main__":
    cik_codes = SECCoverage().getSearchTerms()
    searchingTerms = SearchTerms().getSearchTerms()
    FilingSearcher(ciks=cik_codes, searchTerms=searchingTerms).searchAllFilings()
            