#coding:utf-8
'''
Created on 2017年1月17日

@author: coldJune
'''
from bs4 import BeautifulSoup
import urllib.request
import re

url='https://github.com/coldJune'

def catchLink(url):
    '''
                提 取网页中的超链接
    '''
    links=[]
    html=urllib.request.urlopen(url)
    html=html.read()
    soup=BeautifulSoup(html,'lxml')
    a=soup.findAll('a')
    for link in a:
        links=a['href']
    return
if __name__=='__main__':
    catchLink(url)
