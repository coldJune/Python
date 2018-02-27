#!usr/bin/python3
# -*- coding:UTF-8 -*-

# 导入socket模块和time.ctime()的全部属性
from socket import *
from time import ctime

# 与TCP相同，由于是无连接，所以没有调用监听传入连接
HOST = ''
PORT = 12345
BUFSIZE = 1024
ADDR = (HOST, PORT)

udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)

while True:
    # 进入循环等待消息，一条消息到达时，处理并返回它，然后等待下一条消息
    print('waiting for message...')
    data, addr = udpSerSock.recvfrom(BUFSIZE)
    udpSerSock.sendto(bytes('[%s] %s' % (
        ctime(), data.decode('utf-8')), 'utf-8'), addr)
    print('...received from and returned to:', addr)
