'''
Created on Sep 18, 2016

@author: dave
'''
from SECCoverage import SECCoverage


class Users(object):
    def __init__(self):
        pass
    
    @staticmethod
    def getUsers():
        users = []
        
        users.append(User(name="Gary Chalik", email="gary.chalik@rbccm.com"))
        
        return users
    
    @staticmethod
    def getSearchTerms(user):
        return SECCoverage().getSearchTerms(user)
        
        
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def __str__(self):
        return "User: Name={}, Email={}".format(self.name, self.email)
    