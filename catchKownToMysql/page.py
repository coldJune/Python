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
            request = urllib.request.Request(url)
            response= urllib.request.urlopen(request)
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

    def getGoodAnswer(self,page):
        soup = BeautifulSoup(page)
        text = soup.select('div.good_point div.answer_text pre')
        if len(text) > 0:
            ansText = self.getText(str(text[0]))
            ansText = self.tool.replace(ansText)
            info = soup.select('div.good_point div.answer_tip')
            ansInfo = self.getGoodAnswerInfo(str(info[0]))
            answer = [ansText,ansInfo[0],ansInfo[1],1]
            return answer
        else:
            return None
    def getGoodAnswerInfo(self,html):
        #get the best answer fo author and time
        pattern = re.compile('"answer_tip".*?>(.*?)</a><span class="time.*?>|(.*?)</span>')
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

    def getOtherAnswers(self,page):
        soup = BeautifulSoup(page)
        results = soup.select("div.question_box li.clearfix .answer_info")
        answers = []
        for result in results:
            ansSoup = BeautifulSoup(str(result))
            text = ansSoup.select(".answer_txt span pre")
            ansText = self.getText(str(text[0]))
            ansText = self.tool.replace(ansText)
            info = ansSoup.select(".answer_tj")
            ansInfo = self.getGoodAnswerInfo(info[0])
            answer = [ansText,ansInfo[0],ansInfo[1],0]
            answers.append(answer)
        return answers

    def getAnswer(self,url):
        if not url:
            url = "http://iask.sina.com.cn/b/gQiuSNCMV.html"
        page = self.getPageByURL(url)
        good_ans = self.getGoodAnswer(page)
        other_ans = self.getOtherAnswers(page)
        return [good_ans,other_ans]

page = Page()
page.getAnswer(None)
