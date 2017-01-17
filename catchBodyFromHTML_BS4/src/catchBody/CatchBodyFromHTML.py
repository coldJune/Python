#coding:gbk
'''
Created on 2017年1月17日

@author: coldjune
'''

import glob,os
import requests
from bs4 import BeautifulSoup
import sys
ty=sys.getfilesystemencoding()
url="http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000"
html=requests.get(url)

soup=BeautifulSoup(html.text,"html.parser")
print(soup.body.text.encode('gbk','ignore').decode('gbk'))