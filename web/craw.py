#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# 导入相关的包，其中bs4中的BeautifulSoup负责解析html文档
import os
import sys
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


class Retriever(object):
    """
    从Web下载页面，解析每个文档中的连接并在必要的时候把它们加入"to-do"队列。
    __slots__变量表示实例只能拥有self.url和self.file属性
    """
    __slots__ = ('url', 'file')

    def __init__(self, url):
        """
        创建Retriever对象时调用，将get_file()返回的URL字符串和对
        应的文件名作为实例属性存储起来
        :param url: 需要抓取的连接
        """
        self.url, self.file = self.get_file(url)

    def get_file(self, url, default='index.html'):
        """
         把指定的URL转换成本地存储的更加安全的文件，即从Web上下载这个文件
        :param url: 指定URL获取页面
        :param default: 默认的文件名
        :return: 返回url和对应的文件名
        """
        # 将URL的http://前缀移除，丢掉任何为获取主机名
        # 而附加的额外信息，如用户名、密码和端口号
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc.split('@')[-1].split(':')[0]
        # 将字符进行解码，连接域名创建文件名
        filepath = '%s%s' % (host, urllib.parse.unquote(parsed.path))
        if not os.path.splitext(parsed.path)[1]:
            # 如果URL没有文件扩展名后这将default文件加上
            filepath = os.path.join(filepath, default)
        # 获取文件路径
        linkdir = os.path.dirname(filepath)
        if not os.path.isdir(linkdir):
            # 如果linkdir不是一个目录
            if os.path.exists(linkdir):
                # 如果linkdir存在则删除
                os.unlink(linkdir)
            # 创建同名目录
            os.makedirs(linkdir)
        return url, filepath

    def download(self):
        """
        通过给定的连接下载对应的页面，并将url作为参数调用urllib.urlretrieve()
        将其另存为文件名。如果出错返回一个以'*'开头的错误提示串
        :return: 文件名
        """
        try:
            retval = urllib.request.urlretrieve(self.url, filename=self.file)
        except IOError as e:
            retval = (('***ERROR: bad URL "%s": %s' % (self.url, e)),)
        return retval

    def parse_links(self):
        """
        通过BeautifulSoup解析文件，查看文件包含的额外连接。
        :return: 文件中包含连接的集合
        """
        with open(self.file, 'r', encoding='utf-8') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'html.parser')
        parse_links = []
        for x in soup.find_all('a'):
            if 'href' in x.attrs:
                parse_links.append(x['href'])
        return parse_links


class Crawler(object):
    """
    管理Web站点的完整抓取过程。添加线程则可以为每个待抓取的站点分别创建实例
    """
    # 用于保持追踪从因特网上下载下来的对象数目。没成功一个递增1
    count = 0

    def __init__(self, url):
        """
        self.q 是待下载的连接队列，这个队列在页面处理完毕时缩短，每个页面中发现新的连接则增长
        self.seen 是已下载连接的集合
        self.dom 用于存储主链接的域名，并用这个值判定后续连接的域名与主域名是否一致
        :param url: 抓取的url
        """
        self.q = [url]
        self.seen = set()
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc.split('@')[-1].split(':')[0]
        self.dom = '.'.join(host.split('.')[-2:])

    def get_page(self, url, media=False):
        """
        用于下载页面并记录连接信息
        :param url:
        :param media:
        :return:
        """
        # 实例化Retriever类并传入需要抓取的连接
        # 下在对应连接并取到文件名
        r = Retriever(url)
        fname = r.download()[0]
        if fname[0] == '*':
            print(fname, '....skipping parse')
            return
        Crawler.count += 1
        print('\n(', Crawler.count, ')')
        print('URL:', url)
        print('FILE:', fname)
        self.seen.add(url)
        # 跳过所有非Web页面
        ftype = os.path.splitext(fname)[1]
        if ftype not in ('.htm', '.html'):
            return
        for link in r.parse_links():
            if link.startswith('mailto:'):
                print('...discarded , mailto link')
                continue

            if not media:
                ftype = os.path.splitext(link)[1]
                if ftype in ('.mp3', '.mp4', '.m4av', '.wav'):
                    print('... discarded, media file')
                    continue

            if not link.startswith('http://') and ':' not in link:
                link = urllib.parse.quote(link, safe='#')
                link = urllib.parse.urljoin(url, link)
            print('*', link)
            if link not in self.seen:
                if self.dom not in link:
                    print('... discarded, not in domain')
                else:
                    # 如果没有下载过并且是属于该网站就加入待下载列表
                    if link not in self.q:
                        self.q.append(link)
                        print('...New, added to Q')
                    else:
                        print('...discarded, already in Q')
            else:
                print('...discarded, already processed')

    def go(self, media=False):
        """
        处理所有待下载连接
        :param media:
        :return:
        """
        while self.q:
            url = self.q.pop()
            self.get_page(url, media)


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        try:
            url = input('Enter starting URL:')
        except (KeyboardInterrupt, EOFError):
            url = ''
    if not url:
        return
    if not url.startswith('http://') and not url.startswith('ftp://') and not url.startswith('https://'):
        url = 'http://%s' % url

    robot = Crawler(url)
    robot.go()


if __name__ == '__main__':
    main()

