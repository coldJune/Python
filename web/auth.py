#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import urllib.request
import urllib.error
import urllib.parse

# 初始化过程
# 后续脚本使用的常量
LOGIN = 'wesly'
PASSWD = "you'llNeverGuess"
URL = 'http://localhost:8080/docs/setup.html'
REALM = 'Secure Archive'


def handler_version(url):
    # 分配了一个基本处理程序类，添加了验证信息。
    # 用该处理程序建立一个URL开启器
    # 安装该开启器以便所有已打开的URL都能用到这些验证信息
    hdlr = urllib.request.HTTPBasicAuthHandler()
    hdlr.add_password(REALM,
                      urllib.parse.urlparse(url)[1],
                      LOGIN,
                      PASSWD)
    opener = urllib.request.build_opener(hdlr)
    urllib.request.install_opener(opener=opener)
    return url


def request_version(url):
    # 创建了一个Request对象，在HTTP请求中添加了简单的base64编码的验证头
    # 该请求用来替换其中的URL字符串
    from base64 import encodebytes
    req = urllib.request.Request(url)
    b64str = encodebytes(bytes('%s %s' % (LOGIN, PASSWD), 'utf-8'))[:-1]
    req.add_header("Authorization", 'Basic %s' % b64str)
    return req


for funcType in ('handler', 'request'):
    # 用两种技术分别打开给定的URL，并显示服务器返回的HTML页面的第一行
    print('***Using %s:' % funcType.upper())
    url = eval('%s_version' % funcType)(URL)
    f = urllib.request.urlopen(url)
    print(str(f.readline(), 'utf-8'))
    f.close()
