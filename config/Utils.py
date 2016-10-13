from bs4 import BeautifulSoup
from config import UrlOpen


def getRaw(url):
    html = UrlOpen.UrlOpen().getHTML(url)
    return html

def getsoup(url):
    html = getRaw(url)
    
    if html is None:
        print("No html found for " + url)
        return None
    else:
        soup = BeautifulSoup(html, "lxml")  # a list to hold our urls
        return soup
