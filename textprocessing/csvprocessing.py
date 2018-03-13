#!/usr/bin/python3
# -*- coding:utf-8 -*-
import csv
#  创建需要导入的数据源
DATA = (
    (1, 'Web Clients and Servers', 'base64,urllib'),
    (2, 'Web program：CGI & WSGI', 'cgi, time, wsgiref'),
    (3, 'Web Services', 'urllib,twython'),
)

print('*** WRITTING CSV DATA')
# 打开一个csv文件，使用utf-8编码，同时为了防止写入时附加多的空白行设置newline为空
with open('bookdata.csv', 'w', encoding='utf-8', newline='') as w:
    # csv.writer笑一个打开的文件(或类文件)对象，返回一个writer对象
    # 可以用来在打开的文件中逐行写入逗号分隔的数据。
    writer = csv.writer(w)
    for record in DATA:
        writer.writerow(record)


# writer对象提供一个writerow()方法

print('****REVIEW OF SAVED DATA')
with open('bookdata.csv', 'r', encoding='utf-8') as r:
    # csv.reader()用于返回一个可迭代对象，可以读取该对象并解析为CSV数据的每一行
    # csv.reader()使用一个已打开文件的句柄，返回一个reader对象
    # 当逐行迭代数据时，CSV数据会自动解析并返回给用户
    reader = csv.reader(r)
    for chap, title, modpkgs in reader:
        print('Chapter %s: %r (featureing %s)' % (chap, title, modpkgs))
