#!usr/bin/python3
# -*- coding:UTF-8 -*-

from socket import *

HOST = '127.0.0.1'
PORT = 12345
BUFSIZE = 1024
ADDR = (HOST, PORT)

while True:
    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.connect(ADDR)
    data = input('> ')
    if not data:
        break
    # 因为处理程序类对待套接字通信像文件一样，所以必须发送行终止符。
    # 而服务器只是保留并重用这里发送的终止符
    tcpSocket.send(bytes('%s\r\n' % data, 'utf-8'))
    data = tcpSocket.recv(BUFSIZE)
    if not data:
        break
    # 得到服务器返回的消息时，用strip()函数对其进行处理并使用print()自动提供的换行符
    print(data.decode('utf-8').strip())
    tcpSocket.close()

