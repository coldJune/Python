#!/usr/bin/python3
# -*- coding:utf-8 -*-

import urllib.request as req
import urllib.parse as parse
import os
import uuid
from bs4 import BeautifulSoup
import urllib.error
import sys, getopt
import re


def craw(url, save_path):
    # 从指定单页面下载所有图片
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/48.0.2564.116 '
                      'Safari/537.36 '
                      'TheWorld 7'}
    request = req.Request(url=url, headers=headers)
    html = req.urlopen(request).read();
    html = str(html)
    soup = BeautifulSoup(html, 'lxml')
    noscripts = soup.findAll('noscript')
    imgurls = []
    for noscript in noscripts:
        # 提取图片的URL链接
        img = noscript.find('img')
        url = img['data-original'] if img['data-original'] else ''
        if url != '':
            imgurls.append(url)

    if save_path[0] != '/':
        save_path = './' + save_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if save_path[-1] != '/':
        save_path += '/'

    print('该页面一共有%d张图片' % len(imgurls))
    imgnum = 0
    for imgUrl in imgurls:
        imgnum = imgnum + 1
        picname = save_path + str(uuid.uuid1())+'.jpg'
        print('正在下载%d张' % imgnum)
        try:
            req.urlretrieve(imgUrl, picname)
        except urllib.error.URLError as e:
            if hasattr(e, 'code') or hasattr(e, 'reason'):
                print('第%d张下载失败，其链接地址为%s' % (imgnum, imgUrl))
                continue
        print('第%d张下载成功' % imgnum)


def help():
    # 脚本使用帮助函数
    print("""
        本脚本用于下载单页面中的图片到指定位置
        -h:查看帮助文档
        -p:保存的路径（可选）
        -u:下载的页面URL（必填）
    """)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'hp:u:')
    furl, savepath = '', ''
    for op, value in opts:
        if op == '-u':
            furl = value
        elif op == '-p':
            savepath = value
        elif op == '-h':
            help()
            sys.exit()

    if furl == '':
        print('请输入下载链接，脚本使用方法通过-h查看')
    else:
        craw(furl, savepath)