#!/usr/bin/python3
# -*-  coding:UTF-8 -*-

from atexit import register
import re
import threading
import time
import urllib.request

# 匹配排名的正则表达式
# 亚马逊的网站
REGEX = re.compile(b'#([\d,]+) in Books')
AMZN = 'https://www.amazon.com/dp/'

# ISBN编号和书名
ISBNs = {
    '0132269937': 'Core Python Programming',
    '0132356139': 'Python Web Development with Django',
    '0137143419': 'Python Fundamentals'
}

# 请求头
# 因为亚马逊会检测爬虫,所以需要加上请求头伪装成浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7'
}


def get_ranking(isbn):
    # 爬取网页,获取数据
    # 使用str.format()格式化数据
    url = '{0}{1}'.format(AMZN, isbn)
    # 爬取网页并解析
    req = urllib.request.Request(url, headers=headers)
    page = urllib.request.urlopen(req)
    data = page.read()
    page.close()
    return str(REGEX.findall(data)[0], 'utf-8')


def _show_ranking(isbn):
    # 显示结果
    print('- %r ranked %s' % (ISBNs[isbn], get_ranking(isbn)))


def _main():
    print('At', time.ctime(), 'on Amazon...')
    for isbn in ISBNs:
        (threading.Thread(target=_show_ranking, args=(isbn,))).start()
        #_show_ranking(isbn)


@register
def _atexit():
    # 注册一个退出函数，在脚本退出先请求调用这个函数
    print('all DONE at:', time.ctime())

if __name__ == '__main__':
    _main()