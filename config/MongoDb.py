'''
Created on Sep 18, 2016

@author: dave
'''
from pymongo.mongo_client import MongoClient

class MongoDb(object):
    mongodb = MongoClient()#host="192.168.0.11", port=27017)
    
    def __init__(self):
        pass
    
    def getMongo(self):
        return MongoDb.mongodb 
    
    def getDb(self, name):
        return MongoDb.mongodb[name] 

        #return 