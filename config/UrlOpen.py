from urllib.request import Request, urlopen

headers = {'User-Agent':'Mozilla/5.0'}
results_folder = "results"

class UrlOpen:    
    
    def __init__(self):
        pass
        
    def getHTML(self, url):
        req = Request(url, None, headers)
        html = urlopen(req).read()
       
        return html
    