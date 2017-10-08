import urllib.request as ur
import urllib.error as uerror
import urllib.parse as up
import gzip
import time
from bs4 import BeautifulSoup as bs
import json
import os



URL = 'http://www.hhmmoo.com/manhua19304.html'
INDEX = 'http://www.hhmmoo.com'
DOMAIN = 'http://164.94201314.net/dm03'

def GetVOLs():
    response = ur.urlopen(URL)
    soup = bs(response.read().decode('utf-8'),"html.parser")
    vols = soup.select('ul[class=cVolUl]')[0]
    vols = vols.select('li')
    count = 0
    for item in vols:
        if count < 10:
            count = count+1
            continue
        href = item.select('a')[0]['href']
        title = item.select('a')[0]['title']
        if not os.path.exists(title):
            os.makedirs(title)
        GetImg(title,href)

    pass


def GetImg(title,href):
    response = ur.urlopen(INDEX+href)
    soup = bs(response.read().decode('utf-8'),"html.parser")

    curpage = soup.select('input[name=hdPageIndex]')[0]['value']
    hdVolID = soup.select('input[name=hdVolID]')[0]['value']
    hdPageCount = soup.select('input[name=hdPageCount]')[0]['value']
    hdS = soup.select('input[name=hdS]')[0]['value']
    if int(curpage) > int(hdPageCount):
        return 
    nexthref = '/page'+str(hdVolID)+'/'+str(int(curpage)+1)+'.html?s='+hdS+"&d=0" #set img source
##save the img
    if getCuImg(soup) is not None:
        imgurl = DOMAIN+unsuan(getCuImg(soup))
        filename = title+'/'+str(curpage)+'.jpg'        
        ur.urlretrieve(imgurl,filename)
        print(filename)
    else:
        raise ValueError('not img source')
##
    GetImg(title,nexthref)

def getCuImg(soup):
    if len(soup.select('img[id=img1021]')) != 0:
        return soup.select('img[id=img1021]')[0]['name']
    if len(soup.select('img[id=img2391]')) != 0:
        return soup.select('img[id=img2391]')[0]['name']
    if len(soup.select('img[id=img7652]')) != 0:
        return soup.select('img[id=img7652]')[0]['name']
    if len(soup.select('img[id=imgCurr]')) != 0:
        return soup.select('img[id=imgCurr]')[0]['name']
    return None
    

def unsuan(s):
    x = s[len(s)-1:]
    w="abcdefghijklmnopqrstuvwxyz"
    xi=w.index(x)+1
    sk = s[len(s)-xi-12:len(s)-xi-1]
    s=s[0:len(s)-xi-12]
    k=sk[0:len(sk)-1]
    f=sk[len(sk)-1:]

    for i in range(len(k)):
        old = k[i:i+1]
        new = str(i)
        s = s.replace(old,new)
        #eval("s=s.replace('"+ k[i:i+1] +"','"+ str(i) +"')")
    ss = s.split(f)
    s=""

    for i in range(len(ss)):
        s+=chr(int(ss[i]))
    return s


if __name__ == '__main__':
    GetVOLs()