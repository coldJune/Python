#!usr/bin/python3
# -*- coding:utf-8 -*-

import urllib.request
import urllib.error
import re
import sys
import time
import types
import mysql
import page
import bs4 from BeautifulSoup

class Spider:
    def __init__(self):
        self.page_num = 1
        self.total_num = None
        self.page_spider = page.Page()
        self.mysql = mysql.Mysql()

    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def getPageURLByNum(self,page_num):
        page_url = "`"
