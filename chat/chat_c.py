#!/usr/bin/python3
# -*- coding:UTF-8 -*-

from chat_base import ChatWindowBase
from chat_thread import ChatThread
from socket import *
from time import ctime
import tkinter

HOST = '127.0.0.1'
PORT = 12345
ADDR = (HOST, PORT)
BUFSIZ = 1024


class ChatC(ChatWindowBase):
    def __init__(self):
        super(ChatC, self).__init__()
        self.label.configure(text='客户端')
        self.data = ''
        self.addr = ''
        self.sock = None
        self.receive()

    def send(self, ev=None):
        message = self.chatn.get()
        ChatThread(self.send_c, (message,)).start()
        self.chats.insert('end', '[%s]:to %s' % (ctime(), ADDR))
        self.chats.insert('end', '%s' % message)
        self.chatn.delete(first=0, last=len(message)+1)
        self.top.update()

    def receive(self):
        ChatThread(self.receive_c, ()).start()

    def send_c(self, message):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.sendto(bytes(message, 'utf-8'), ADDR)

    def receive_c(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(ADDR)
        while True:
            self.data, self.addr = self.sock.recvfrom(BUFSIZ)
            self.chats.insert('end', '[%s]:from %s' % (ctime(), ADDR))
            self.chats.insert('end', '%s' % self.data)
            self.top.update()


def main():
     c = ChatC()
     tkinter.mainloop()


if __name__ == '__main__':
    main()
