#!usr/bin/python3
# -*- coding:UTF-8 -*-

# 导入socketserver相关的类和time.ctime()的全部属性
from socketserver import (TCPServer as TCP,
                          StreamRequestHandler as SRH)
from time import ctime

HOST = ''
PORT = 12345
ADDR = (HOST, PORT)


class MyRequestHandler(SRH):
    # MyRequestHandler继承自StreamRequestHandler

    def handle(self):
        # 重写handle方法，当接收到一个客户端消息是，会调用handle()方法
        print('...connected from:', self.client_address)
        # StreamRequestHandler将输入和输出套接字看做类似文件的对象
        # 所以使用write()将字符串返回客户端，用readline()来获取客户端信息
        self.wfile.write(bytes('[%s] %s' % (
            ctime(), self.rfile.readline().decode('utf-8')), 'utf-8'))

# 利用给定的主机信息和请求处理类创建了TCP服务器
# 然后无限循环地等待并服务于客户端请求
tcpServ = TCP(ADDR, MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()
