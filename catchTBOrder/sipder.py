#!/usr/bin/python3 
#-*- coding:utf-8 -*-


import urllib
import http.cookiejar
import requests
import webbrowser

class Taobao:
    
    def __init__(self):
        self.loginUrl='https://login.taobao.com/member/login.jhtml'
        self.proxyUrl='http://111.155.116.210:8123'
        self.loginHeaders={
            'Host':'login.taobao.com',
            'User-Agent':'''Mozilla/5.0 (Windows NT 10.0; Win64; x64)
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100
            Safari/537.36''',
            'Referer':'https://login.taobao.com/member/login.jhtml',
            'Content-Type':'application/x-www-form-urlencoded',
            'Connection':'keep-alive'
        }
        self.username='还是过于单纯'
        self.ua=''''''
        self.password2=''
        self.post={
            'ua':self.ua,
            'TPL_checkcode':'',
            'CtrlVersion': '1,0,0,7',
            'TPL_password':'',
            'TPL_redirect_url':'''https://member1.taobao.com/member/fresh/account_security.htm?sp
                                m=a1z02.1.a210b.d1000356.3c2d6a48dGsvSU&tracelog=m
                                ytaobaonavsetup&nekot=1470211439696''',
            'TPL_username':self.username,
            'loginsite':'0',
            'newlogin':'0',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support':'000001',
            'loginType':'4',
            'minititle':'',
            'minipara':'',
            'umto':'NaN',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
        }
        self.postData=urllib.urlencode(self.post)
        self.proxy=urllib.
