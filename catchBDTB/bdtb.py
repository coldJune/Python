#!/usr/bin/python3
# -*- coding:utf-8 -*-

import urllib
import urllib.error
import urllib.request
import re
import os

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
            print(url)
            page=str(response,'utf-8')
            #print(response.read())
            return page
        except urllib.error.URLError as e:
            if(hasattr(e,"reason")):
                print("连接百度贴吧失败，错误原因",e.reason)
                return None
    
    def getTile(self,page):
        pattern=re.compile(r'<h3 class="core_title_txt pull-left(?:.*?)>(.*?)</h3>')
        result=pattern.search(page)
        if result:
            #print(result.group(1))
            return result.group(1).strip()
        else:
            return None
     
    def getPageNum(self,page):
        pattern=re.compile(r'''<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>''')
        result=pattern.search(page)
        #print(result)
        if result:
            #print(result.group())
            return result.group(1)
        else:
            return None

    def getContent(self,page):
        pattern=re.compile(r'<div id="post_content_.*?">(.*?)</div>')
        result=pattern.findall(page)
        contents=[]
        for floor in result:
            #print(floorNum,r"楼-------------------------------------------------------------------")
            #print(self.tool.replace(floor))
            content="\n"+self.tool.replace(floor)+"\n"
            contents.append(content.encode('utf-8'))
        return contents
    def setFileTitle(self,title):
        if not os.path.exists('./content'):
            os.mkdir("./content")
        if title is not None:
            self.file=open('./content/'+title+".txt","w+")
        else:
            self.file=open('./content/'+self.defaultTitle+".txt","w+")

    def writeData(self,contents):
        for item in contents:
            if self.floorTag==1:
                floorLine="\n"+str(self.floorNum)+u"-------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(str(item,'utf-8'))
            self.floorNum+=1

    def start(self):
        indexPage=self.getPage(1)
        pageNum=self.getPageNum(indexPage)
        title=self.getTile(indexPage)
        self.setFileTitle(title)
        if pageNum  is None:
            print("URL已失效，请重试")
            return
        try:
            print("该帖子共有"+str(pageNum)+"页")
            for i in range(1,int(pageNum)+1):
                print("正在写入"+str(i)+"页")
                page=self.getPage(i)
                contents=self.getContent(page)
                self.writeData(contents)
        except IOError as e:
            print("写入异常，原因"+e.message)
        finally:
            print("写入完成")

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


