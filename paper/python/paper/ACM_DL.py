'''
Created on 2015年12月1日

@author: cdz
'''

import time
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup


def getHtml(keyword, page_num):
    keyword = keyword.replace(' ', '%20')
    url = 'http://dl.acm.org/results.cfm?query=' + keyword + '&start=' + str(20 * (page_num - 1)) + '&filtered=&within=owners%2Eowner%3DACM&dte=&bfr=&srt=_score'
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36')
    
    while True:
        try:
            page = urlopen(req, timeout=15)
            break
        except Exception as e:
            print(e)
    html = page.read()
    return html

def getTitleAndPath(thediv):
    divsoup = BeautifulSoup(str(thediv), 'html.parser')
    titlediv = divsoup.find('div', 'title')
    title = titlediv.a.string
    alist = divsoup.find_all('a')
    pdfLinkList = [a for a in alist if 'name' in a.attrs.keys()]
    if len(pdfLinkList) < 1:
        path = None
    else:
        path = pdfLinkList[0].attrs['href']
    return title, path

def download(title, path, folder):
    print('try to download', title, path)
    host = 'http://dl.acm.org/'
    url = host + path
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36')
    while True:
        try:
            page = urlopen(req, timeout=10)
            pdfbytes = page.read()
            break
        except Exception as e:
            time.sleep(15)
            print(e)
    filename = getFileName(title)
    f = open(folder + filename, 'wb')
    f.write(pdfbytes)
    f.close()
    
def getFileName(title):
    file_name = title + '.pdf'
    file_name = file_name.replace('\\', '')
    file_name = file_name.replace('/', '')
    file_name = file_name.replace(':', '')
    file_name = file_name.replace('*', '')
    file_name = file_name.replace('?', '')
    file_name = file_name.replace('\"', '')
    file_name = file_name.replace('<', '')
    file_name = file_name.replace('>', '')
    file_name = file_name.replace('|', '')
    return file_name

def start(keyword, page_from, page_to, folder, delay):
    for page in range(page_from, page_to + 1):
        while True:
            try:
                html = getHtml(keyword, page)
                break
            except Exception:
                pass
        soup = BeautifulSoup(html, 'html.parser')
        divList = soup.find_all('div', {'class' : 'details'})
        title2path = {}
        for thediv in divList:
            title, path = getTitleAndPath(thediv)
            if path != None:
                title2path[title] = path
        papernum = len(title2path)
        i = 1
        for title, path in title2path.items():
            print('downloading paper' , str(i), '/', str(papernum), 'in page', str(page), '/', str(page_to))
            download(title, path, folder)
            time.sleep(delay)
            i += 1
            
    
if __name__ == '__main__':
    start('recommendation', 1, 3, 'd:/p/')
    
    
    
    


