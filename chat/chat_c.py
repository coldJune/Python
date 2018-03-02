#!/usr/bin/python3
# -*- coding:UTF-8 -*-

from chat_base import ChatWindowBase
from chat_thread import ChatThread
from socket import *
from time import ctime


HOST = ''
PORT = 12345
ADDR = (HOST, PORT)
BUFSIZ = 1024

class ChatC(ChatWindowBase):
    def __init__(self):
        super.__init__()
        self.receive()

    def send(self):
        message = self.chatn.getvar()
        ChatThread(self.send_c, (message,)).start()
        self.chats.setvar('%s:\t\tto %s\n%s' % (ctime(), ADDR, message))

    def receive(self):
        ChatThread(self.receive_c).start()
        self.chats.setvar('%s:\t\tfrom %s\n%s' % (ctime(), ADDR, self.data))

    def send_c(self, message):
        udpSocket = socket(AF_INET, NI_DGRAM)
        udpSocket.sendto(message, ADDR)
        pass

    def receive_c(self):
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        while True:
            self.data, self.addr = udpSocket.recvfrom(BUFSIZ)
            