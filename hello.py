import re
import urllib2
from bs4 import BeautifulSoup

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def isValidUrl(url):
    if regex.match(url) is not None:
        return True;
    return False

def crawler(SeedUrl,textfile):
    tocrawl=[SeedUrl]
    crawled=[]
    while tocrawl:
        page=tocrawl.pop()
        try:
            urllib2.urlopen(page)
        except:
            continue
        pagesource=urllib2.urlopen(page)
        s=pagesource.read()
        soup=BeautifulSoup(s)
        links=soup.findAll('a',href=True)
        if page not in crawled:
            for l in links:
                if isValidUrl(l['href']):
                    tocrawl.append(l['href'])
            crawled.append(page)
            textfile.write(page+'\n')
            print page
    return crawled
textfile = file('depth.txt','wt')
SeedUrl = input("--> ")
crawler(SeedUrl,textfile)
textfile.close()