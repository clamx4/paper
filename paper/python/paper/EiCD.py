'''
Created on 2015年12月6日

@author: cdz
'''


from urllib.request import Request, urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def getHtml(keyword='recommendation'):
    host = 'http://www.engineeringvillage.com'
    path = '/search/submit.url'
    url = host + path
    data = {'CID' : 'searchSubmit',
            'resetDataBase' : '1',
            'searchtype' : 'Expert',
            'origin' : 'searchform',
            'category' : 'expertsearch',
            'database' : '1',
            'searchWord1' : keyword,
            'search' : 'Search',
            'yearselect' : 'yearrange',
            'startYear' : 1969,
            'endYear' : 2016,
            'stringYear' : 'CSY1884CST1969',
            'updatesNo' : '1',
            'sort' : 'relevance',
            'autostem' : 'true',
            '_sourcePage' : 'sMDIshoFqCrVWMYCskH10-_VEpYoCxgP2pgp04XxfpJQa6xCjIm9jG_PZbTGMKxQXLp8R9a1vQA=',
            '__fp' : 'nFXjcIHaAMEsF-y_4R_hhsFDnMhaPLuXrrMJK0nL9SSs4IpouqpBC7OO-VtsXQz2'
            }
    req = Request(url, urlencode(data).encode(encoding='utf_8', errors='strict'))
    page = urlopen(req)
    print(page.getheaders())
    return page.read()

def get_docID(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    
if __name__ == '__main__':
    url = 'http://www.engineeringvillage.com/search/results/fulltext.url?docID=cpx_M3b711cc01513a0f689fM4a8710178163171'
    url = 'http://www.engineeringvillage.com/search/results/fulltext.url?docID=cpx_M67b7e7f3150d9209f33M683310178163171'
    req = Request(url)
    #req.add_header('Cookie', 'CLIENTID=65ca056fMf9ebM4805M9cb6Md568a64315d9; utt=0ed6-3b43095715185001287-005097d9a7efd5fd-r8; SECUREID=47614044Mab73M4ef0M9887M19de94227c8d-4bb36f5177aa742865eea729525e611e; CARS_COOKIE=0077002B00550038003000670062005100750043006A006E002F00670057006800390033006300590043004C005A0033006400640048004800300065006F0041004C003300620033007300460064003900520049005700750046004B004C006E0056002B00660041004C0070006B006A004E006A005100390057006B00760061004E006D00640035006F0068002F0039006A004D004100620068005400650076004700520031005A007000760079004C007100550056004300330041004F002F0075003500580035003400700064002F0037003900590058004C00300071007A00580034006C00550067004900520058004200480051004E007A004F0039005A00580052004200350050007A0031006D0059005000450062002B004800450063005800660044007600610077003D003D; RXSESSION=5181-8c678118151374909641631652040f986f4-QJ; JSESSIONID=B7DE6DAC963D7E5C13E33496F88D704A.PA9NYTnBhzyWMSWsBc0gpg; AWSELB=C5B163BF0829A4594B41E3AE2B6A7BC8C235E44B0443D28BD48772950F3A6669185D570080D8AC738F9FF68988989A1956979EEB425C37E628F50F984BA6873BB2867BE40CDF1D3C86780C90575ACA1D0231275C47; acw=4181-8c678118151374909641631652040f986f4-O%7C%24%7CPUOWE4FQed%2BIEzQgROX6KNmU3A0uymse1F4%2BDnb6LoIH7F2o89Aon%2FNkgUvplASbOhpWJnCLyI%2FUkJl%2FywmQezV6UuEmh3k95ic3jrADPgQ%3D; ev_dldpref=null; EISESSION="0_b8a4eeb2Mef27M41c1Ma8c9Mf179f02cfc11:i-f57dee4b_2015-12-08 07:22:05_1ba364d705ea1e02201d1d3b9b588c64"')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36')
    
    html = urlopen(req).read()
    
    f = open('d:/1.htm', 'wb')
    f.write(html)
    f.close()
    
    
    
    
    
    
    
    
    
    