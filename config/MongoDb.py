'''
Created on Sep 18, 2016

@author: dave
'''
from pymongo.mongo_client import MongoClient

        
from enum import Enum
class Env(Enum):
    local = None
    dev = "mongodb://dado0583:selecta@edgarsearch-shard-00-00-hcsdn.mongodb.net:27017,edgarsearch-shard-00-01-hcsdn.mongodb.net:27017,edgarsearch-shard-00-02-hcsdn.mongodb.net:27017/admin?ssl=true&replicaSet=EdgarSearch-shard-0&authSource=admin"
    

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