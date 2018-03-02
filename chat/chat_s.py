#!/usr/bin/python3
#  -*- coding:UTF-8 -*-

from chat_base import ChatWindowBase
from chat_thread import ChatThread
from socket import *
from time import ctime


HOST = ''
PORT = 123456
ADDR = (HOST, PORT)

BUFSIZ = 1024


class ChatS(ChatWindowBase):
    def __init__(self):
        super.__init__()
        self.receive()

    def send(self):
        message = self.chatn.get()
        ChatThread(self.send_t, message, self.addr).start()
        self.chats.setvar('%s:\t\tto %s\n %s\n' % (ctime(), self.addr, message))

    def receive(self):
        ChatThread(self.receive_t).start()

    def send_t(self, message):
        udpsocket = socket(AF_INET, SOCK_DGRAM)
        udpsocket.sendto(message, self.addr)

    def receive_t(self):
        while True:
            udpsocket = socket(AF_INET, SOCK_DGRAM)
            self.receiveData, self.addr = udpsocket.recvfrom(BUFSIZ)
            self.chats.setvar('%s:\t\tfrom %s\n %s\n' % (ctime(), self.addr, self.receiveData))

