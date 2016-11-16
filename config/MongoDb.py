'''
Created on Sep 18, 2016

@author: dave
'''
from pymongo.mongo_client import MongoClient

        
from enum import Enum
class Env(Enum):
    local = None
    dev = "mongodb://edgar:edgar@ds153637.mlab.com:53637/edgar"
    
class MongoDb(object):
    #mongodb = MongoClient()#host="192.168.0.11", port=27017)
    
    def __init__(self, env = Env.local):
        if env is Env.dev:
            self.mongodb = MongoClient(Env.dev.value)
        else:
            self.mongodb = MongoClient()
    
    def getMongo(self):
        return self.mongodb 
        
    def getDb(self, name):
        return self.mongodb[name] 

        #return 