'''
Created on Sep 18, 2016

@author: dave
'''
import concurrent.futures
import os
import sys
import zlib

try:
    sys.path.index(os.getcwd()) # Or os.getcwd() for this directory
except ValueError:
    sys.path.append(os.getcwd()) # Or os.getcwd() for this directory
    
from sec_config.Coverage import SECCoverage
from sec_config.SearchTerms import SearchTerms
from config.MongoDb import MongoDb


class FilingSearcher(object):
    domain = 'https://www.sec.gov'
    baseUrl = domain+ '/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=&dateb=&owner=exclude&start={}&count={}'    
        
    def __init__(self, filingType="All", ciks=[], searchTerms=[]):
        self.filingType=filingType
        self.ciks=ciks
        self.searchTerms=searchTerms

        #pool.submit(outputRaceResults, url)  
            
    def searchFilings(self):   
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:             
            for cik in self.ciks:
                pool.submit(self.searchFiling, self.searchTerms, cik)  
                #self.searchFiling(cik)
                        
    def searchFiling(self, searchTerms, cik):
        try:
            print('Searching filings for CIK:{}'.format(str(cik)))                
            filingsCollection = MongoDb().getDb('sec')['filings']
            searchCollection = MongoDb().getDb('sec')['searchresults']
            
            collection = filingsCollection.find({"cik":cik}, {"RawText":1, "_id":1})
            
            for item in collection:            
                text = zlib.decompress(item['RawText']).decode("utf-8")
                    
                matches = self.findMatches(text, searchTerms)
                if len(matches)>0:
                    print("Matches for {} (ID={}) are {}".format(cik, item['_id'], matches))
                    resultsData = {}
                    resultsData["_id"] = item['_id']                
                    resultsData["cik"] = cik
                    resultsData["matches"] = matches
                    searchCollection.save(resultsData)
        
        except Exception as e:
            logging.exception(e)
            print(str(e))

  
    def findMatches(self, item, searchTerms):
        matches = {}
        for bucket in searchTerms:
            for string in searchTerms[bucket]:
                if string in item:
                    if bucket not in matches or len(matches[bucket]) == 0:
                        matches[bucket] = []
                    
                    matches[bucket].append(string)
                    
        return matches
            
cik_codes = SECCoverage().getSearchTerms()
searchingTerms = SearchTerms().getSearchTerms()
FilingSearcher(ciks=cik_codes, searchTerms=searchingTerms).searchFilings()
            