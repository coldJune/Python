#!usr/bin/python3
# -*- coding:UTF-8 -*-

from socket import *

HOST = '127.0.0.1'
PORT = 12345
BUFSIZE = 1024
ADDR = (HOST, PORT)

udpClienSock = socket(AF_INET, SOCK_DGRAM)

while True:
    data = bytes(input('>'), 'utf-8')
    if not data:
        break
    udpClienSock.sendto(data, ADDR)
    data, ADDR = udpClienSock.recvfrom(BUFSIZE)
    if not data:
        break
    print(data.decode('utf-8'))
udpClienSock.close()
