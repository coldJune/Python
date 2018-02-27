#!usr/bin/python3
# -*- coding: UTF-8 -*-

# 导入socket模块所有属性
from socket import *

# 服务器的主机名
# 服务器的端口号,应与服务器设置的完全相同
# 缓冲区大小为1KB
HOST = '127.0.0.1'
PORT = 12345
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 分配了TCP客户端套接字
# 主动调用并连接到服务器
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    # 无限循环，输入消息
    data = bytes(input('> '), 'utf-8')
    if not data:
        # 消息为空则退出循环
        break
    # 发送输入的信息
    # 接收服务器返回的信息，最后打印
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZE)
    if not data:
        # 消息为空则退出循环
        break
    print(data.decode('utf-8'))
# 关闭客户端
tcpCliSock.close()
