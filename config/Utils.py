from bs4 import BeautifulSoup
from htmlCache import UrlOpen

def getsoup(url):
    html = UrlOpen.UrlOpen().getHTML(url)
    
    if html is None:
        print("No html found for " + url)
        return None
    else:
        soup = BeautifulSoup(html, "lxml")  # a list to hold our urls
        return soup
