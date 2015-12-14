'''
Created on 2015年11月22日

@author: zz
'''

import json
import time

from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode

def getCookies(url = 'http://ieeexplore.ieee.org'):
    while True:
        try:
            resp = urlopen(url, timeout=10)
            break
        except Exception as e:
            print('exception when getting cookie:', e)
            time.sleep(10)
    cookies = resp.headers.get_all('Set-Cookie')
    return cookies
        
def newRequest(cookies, keyword, page = 1):
    host = 'http://ieeexplore.ieee.org'
    reqPath = '/rest/search'
    data = {'queryText' : keyword,
            'refinements' : [],
            'searchWithin' : [],
            'newsearch' : 'true',
            'pageNumber':str(page),
            "searchField":"Search_All"
            }
    req = Request(host + reqPath)
    req.add_header('Host', 'ieeexplore.ieee.org')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Content-Length', str(len(str(data))))
    req.add_header('Accept', 'application/json, text/plain, */*')
    req.add_header('Origin', 'http://ieeexplore.ieee.org')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')
    req.add_header('Content-Type', 'application/json;charset=UTF-8')
    req.add_header('Referer', 'http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=recommendation&newsearch=true')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.8')
    req.add_header("Cookie", '; '.join(cookies))
    return req, data

def getQuery(cookies, keyword, pageNum, delay):
    req, data = newRequest(cookies, keyword, pageNum)
    while True:
        try:
            resp = urlopen(req, json.dumps(data).encode(encoding='utf_8'), timeout=10)
            resp_str =  str(resp.read(), encoding = 'utf-8')
            break
        except Exception as e:
            print('error when query:', e)
            raise e
    return json.loads(resp_str)

def do_record(record, keyword):
    recordUrl = 'http://cloud.flyingff.net/resource/record.php'
    data = {'record' : record,
            'keyword' : keyword
            }
    req = Request(recordUrl)
    res = urlopen(req, urlencode(data).encode(encoding='utf_8'))
    print(res.read())
    
def record_in_mem(record, recordlist):
    recordlist.append(record)
    print(''.join(['record:', json.dumps(record)]))

def spide_url(keyword, page_from, page_to, folder_path, delay):
    while True:
        try:
            cookies = getCookies()
            break
        except Exception:
            pass
    host = 'http://ieeexplore.ieee.org'
    for pageNum in range(page_from, page_to + 1):
        while True:
            try:
                pageJson = getQuery(cookies, keyword, pageNum, delay)
                break
            except Exception:
                time.sleep(delay)
                cookies = getCookies()
        i = 1
        for record in pageJson['records']:
            print('getting', i, '/', len(pageJson['records']), 'paper URL in ', pageNum, '/', page_to, 'page')
            preview = record['pdfLink']
            req = Request(host + preview)
            req.add_header('Cookie', '; '.join(cookies))
            
            while True:
                try:
                    pdfPage = urlopen(req, timeout=10)
                    html = str(pdfPage.read(), encoding = 'utf-8')
                    arr = html.split(sep='<frame src=\"')
                    pdfUrl = arr[2].split(sep='\"')[0]
                    record['pdfUrl'] = pdfUrl
                    break
                except Exception as err:
                    print(err)
#                     f = open('d:\\1.htm','w')
#                     f.write(html)
#                     f.close()
                    print('maybe download too excessively, waiting for', delay, 's')
                    time.sleep(delay)
                    cookies = getCookies()
                    
            download(record, folder_path, cookies, delay)
            time.sleep(delay)
            i += 1
            
            
def download(record, folder_path, cookies, delay):
    url = record['pdfUrl']
    file_name = ''.join((record['title'], '.pdf'))
    file_name = file_name.replace('\\', '')
    file_name = file_name.replace('/', '')
    file_name = file_name.replace(':', '')
    file_name = file_name.replace('*', '')
    file_name = file_name.replace('?', '')
    file_name = file_name.replace('\"', '')
    file_name = file_name.replace('<', '')
    file_name = file_name.replace('>', '')
    file_name = file_name.replace('|', '')
    
    
    req = Request(url)
    #cookies = getCookies()
    req.add_header('Cookie', '; '.join(cookies))
    
    print('downloading:', file_name)     
    while True:
        try:
            page = urlopen(req, timeout=10)
            html = page.read()
            break
        except Exception as err:
            print('error when downloading:', err)
            print("maybe download too excessively, waiting for", delay, "s")
            req = Request(url)
            cookies = getCookies()
            req.add_header('Cookie', '; '.join(cookies))
            time.sleep(delay)
    
    file = open(''.join((folder_path, file_name)), mode='wb')
    file.write(html)
    file.close()



if __name__ == '__main__':
    pass
            
    
    
    
