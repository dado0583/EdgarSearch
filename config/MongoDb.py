'''
Created on Sep 18, 2016

@author: dave
'''
from pymongo.mongo_client import MongoClient

class MongoDb(object):
    #mongodb = MongoClient()#host="192.168.0.11", port=27017)
    
    mongodb = MongoClient("mongodb://dado0583:selecta@edgarsearch-shard-00-00-hcsdn.mongodb.net:27017,edgarsearch-shard-00-01-hcsdn.mongodb.net:27017,edgarsearch-shard-00-02-hcsdn.mongodb.net:27017/admin?ssl=true&replicaSet=EdgarSearch-shard-0&authSource=admin")
    
    def __init__(self):
        pass
    
    def getMongo(self):
        return MongoDb.mongodb 
    
    def getDb(self, name):
        return MongoDb.mongodb[name] 

        #return 