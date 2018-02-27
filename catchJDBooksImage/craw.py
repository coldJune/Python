#!/usr/bin/python3
# -*- coding:utf-8 -*-

import re
import urllib.request
import urllib.error
import urllib.parse
import os

sum=0
def craw(url,page):
    html=urllib.request.urlopen(url).read()
    html=str(html)
    re1=r'<div id="plist".+?<div class="page clearfix">'
    result=re.compile(re1).findall(html)
   # result=str(result)
    if result is not None:
        result=result[0]
    else:
        return 
    re2=r'''<img width="200" height="200" data-img="1" src="//(.+?\.jpg)">|<img
    width="200" height="200" data-img="1"data-lazy-img="//(.+?\.jpg)">'''
    imagelist=re.compile(re2).findall(result)
    x=1
    global sum
    if(not os.path.exists('./books')):
        os.mkdir('./books')
    for imageurl in imagelist:
        imagename='./books/'+str(page)+'_'+str(x)+'.jpg'
        #print(imagename)
        num=0 if imageurl[0]!='' else 1
        print(num)
        imgurl='http://'+imageurl[num]
        print(imgurl)
        print('开始爬第%d页第%d张图片'%(page,x))
        try:
            urllib.request.urlretrieve(imgurl,imagename)
        except urllib.error.URLError as e:
            if hasattr(e,'code') or hasattr(e,'reason'):
             x+=1
        print('成功保存第%d页第%d张图片'%(page,x))
        x+=1
        sum+=1
    


    
