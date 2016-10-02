'''
Created on Sep 18, 2016

@author: dave
'''

class SearchTerms(object):
    def __init__(self):
        pass
    
    
    def getSearchTerms(self, user="All"):
        buckets = {}
        
        buckets['Foreign Currency'] = [
                "Currency Exchange Forward",
                "Currency Forward",
                "Currency Swap",
                "Currency Derivative",
                "Currency Future",
                "Currency Contract",
                "Currency Cash flow hedge",
                "Currency Cashflow hedge",
                "Foreign Exchange Exchange Forward",
                "Foreign Exchange Forward",
                "Foreign Exchange Swap",
                "Foreign Exchange Derivative",
                "Foreign Exchange Future",
                "Foreign Exchange Contract",
                "Foreign Exchange Cash flow hedge",
                "Foreign Exchange Cashflow hedge",
                "FX Forward",
                "FX Forward",
                "FX Swap",
                "FX Derivative",
                "FX Future",
                "FX Contract",
                "FX Cash flow hedge",
                "FX Cashflow hedge"
            ]

        buckets['Interest Rates'] = [
                "Interest Rate Swap",
                "Interest Rate Contract",
                "Interest Rate Derivative",
                "Interest Rate Forward",
                "Interest Rate Future",
                "Interest Rate Cash flow hedge",
                "Interest Rate Cashflow hedge",
                "IR Swap",
                "IR Contract",
                "IR Derivative",
                "IR Forward",
                "IR Future",
                "IR Cash flow hedge",
                "IR Cashflow hedge"
            ]

        buckets['Commodities'] = [
                "Commodity Swap",
                "Commodity Contract",
                "ICommodity Derivative",
                "Commodity Forward",
                "Commodity Future",
                "Commodity Cash flow hedge",
                "Commodity Cashflow hedge",
                "Commodities Swap",
                "Commodities Contract",
                "Commodities Derivative",
                "Commodities Forward",
                "Commodities Future",
                "Commodities Cash flow hedge",
                "Commodities Cashflow hedge"
            ]

        buckets['Misc'] = [
                "Derivatives Financial Instrument",
                "Forward Contract"
            ]
                
        return buckets
    
        
        