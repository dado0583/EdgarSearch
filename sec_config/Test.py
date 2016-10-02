'''
Created on Sep 18, 2016

@author: dave
'''
from SECCoverage import SECCoverage
from config import MongoDb
from users.Users import Users


if __name__ == '__main__':
    mongo = MongoDb.MongoDb().getMongo()
    
    coverage = SECCoverage.getSearchTerms("Empty")
    print(coverage)
    
    users = Users.getUsers()
    
    print(users[0])
    coverage = Users.getSearchTerms(users[0])
    
    print(coverage)
    
    print(mongo.database_names())