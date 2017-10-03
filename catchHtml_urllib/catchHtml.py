#!/usr/bin/python3

import urllib.request
import os

def readHtml():
    file=urllib.request.urlopen('https://www.baidu.com')
    data=file.read()
    dataline=file.readline()
    if(not os.path.exists('./html')):
        os.mkdir('./html')
    with open('./html/1.html','wb') as fhandle:
        fhandle=open('./html/1.html','wb')
        fhandle.write(data)
