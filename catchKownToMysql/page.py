#!usr/bin/python3
# -*- coding:utf-8 -*-

import urllib.request
import urllib.error
import urllib
import re
import time
import tool
import types
from bs4 import BeautifulSoup

class Page:
    #get the answer from page
    def __init__(self):
        self.tool = tool.Tool()

    
    def getCurrentDate(self):
        #get current date
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def getCurrentTime(self):
        #get current time
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))


    def getPageByURL(self,url):
        #get whole page form url
        try:
            request = urllib.Request(url)
            response= urllib.urlopen(request)
            return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print(self.getCurrentTime(),'获取问题页面失败，错误代号',e.code)
                return None
            if hasattr(e,"reason"):
                print(self.getCurrentTime(),'获取问题页面失败，原因',e.reasn)

    def getText(self,html):
        #get the question
        if not type(html) is types.StringType:
            html = str(html)
        pattern = re.compile('<pre.*?>(.*?)<.*?/pre>')
        match = re.search(pattern,html)
        if match:
            return match.group(1)
        else:
            return None

    def getGoodAnswerInfo(self,html):
        #get the best answer fo author and time
        pattern re.compile('"answer_tip".*?>(.*?)</a><span class="time.*?>|(.*?)</span>')
        match = re.search(pattern,html)
        if match:
            time = macth.group(2)
            time_pattern = re.compile('\d{2}-\d{2}-\d{2}',re.S)
            time_match = re.search(time_pattern,time)
            if not time_match:
                time = self.getCurrentDate()
            else:
                time  = "20"+time
            return [match.group[1],time]
        else:
            return [Noen,None]

