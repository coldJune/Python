#!usr/bin/python3
# -*- coding:UTF-8 -*-

# 导入socket模块和time.ctime()的所有属性
from socket import *
from time import ctime

# HOST变量是空白，这是对bind()方法的标识，标识它可以使用任何可用的地址
# 选择一个随机的端口号
# 缓冲区大小为1KB
HOST = ''
PORT = 12345
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 分配了TCP服务套接字
# 将套接字绑定到服务器地址
# 开启TCP的监听调用
# listen()方法的参数是在连接被转接或拒绝之前，传入连接请求的最大数
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    # 服务器循环，等待客户端的连接的连接
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connected from:', addr)

    while True:
        # 当一个连接请求出现时，进入对话循环，接收消息
        data = tcpCliSock.recv(BUFSIZE)
        if not data:
            # 当消息为空时，退出对话循环
            # 关闭客户端连接，等待下一个连接请求
            break
        tcpCliSock.send(bytes('[%s] %s' % (
            ctime(), data.decode('utf-8')), 'utf-8'))

    tcpCliSock.close()
