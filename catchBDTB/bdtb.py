#!/usr/bin/python3
# -*- coding:utf-8 -*-

import urllib
import urllib.error
import urllib.request
import re

class BDTB:
    #the class for catch baidutieba
    def __init__(self,baseUrl,seeLZ,floorTag):
        #init method
        #Input:baseUrl
        #
        #Input:seeLZ
        self.baseUrl=baseUrl
        self.seeLZ='?see_lz='+str(seeLZ)
        self.tool=Tool()
        self.floorNum=1
        self.defaultTitle=r"百度贴吧"
        self.floorTag=floorTag

    def getPage(self,pageNum):
        try:
            url=self.baseUrl+self.seeLZ+'&pn='+str(pageNum)
            request=urllib.request.Request(url)
            response=urllib.request.urlopen(request).read()
            page=str(response,'utf-8')
            #print(response.read())
            return page
        except urllib.error.HTTPError as e:
            if(hasattr(e,"reason")):
                print("连接百度贴吧失败，错误原因",e.reason)
                return None
    
    def getTile(self,page):
        page=self.getPage(page)
        pattern=re.compile(r'<h3 class="core_title_txt pull-left(?:.*?)>(.*?)</h3>')
        result=pattern.search(page)
        if result:
            #print(result.group(1))
            return result.group().strip()
        else:
            return None
     
    def getPageNum(self):
        page=self.getPage(1)
        pattern=re.compile(r'''<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>''')
        result=pattern.search(page)
        #print(result)
        if result:
            #print(result.group())
            return result.group(1)
        else:
            return None

    def getContent(self,page):
        page=self.getPage(page)
        pattern=re.compile(r'<div id="post_content_.*?">(.*?)</div>')
        result=pattern.findall(page)
        floorNum=1
        for floor in result:
            print(floorNum,r"楼-------------------------------------------------------------------")
            print(self.tool.replace(floor))
            floorNum+=1

class Tool:
    #deal with the label of each page

    #remove<img>
    removeImg=r'<img.*?>| {7}|'

    #removeAddr
    removeAddr=r'<a.*?>|</a>'

    #replace to \n
    replaceLine=r'<tr>|<div>|</div>|<p>'

    #replace td
    replaceTD=r'<td>'
    #add two space at the head of paragraph
    replacePara=r'<p.*?>'

    #replace <br> to \n
    replaceBR=r'<br><br>|<br>'

    #remove other label
    removeExtraTag=r'<.*?>'

    def replace(self,x):
        x=re.sub(self.removeImg,'',x)
        x=re.sub(self.removeAddr,'',x)
        x=re.sub(self.replaceLine,r'\n',x)
        x=re.sub(self.replacePara,r"\n  ",x)
        x=re.sub(self.replaceTD,r'\t',x)
        x=re.sub(self.replaceBR,r'\n',x)
        x=re.sub(self.removeExtraTag,'',x)
        return x.strip()

baseUrl="https://tieba.baidu.com/p/3719151137"
bdtb=BDTB(baseUrl,1)
bdtb.getContent(1)

