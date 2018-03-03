#!/usr/bin/python3
#  -*- coding:UTF-8 -*-

from chat_base import ChatWindowBase
from chat_thread import ChatThread
from socket import *
from time import ctime
import tkinter

HOST = ''
PORT = 12345
ADDR = (HOST, PORT)

BUFSIZ = 1024


class ChatS(ChatWindowBase):
    def __init__(self):
        super(ChatS, self).__init__()
        self.label.configure(text='服务器')
        self.receiveData = ''
        self.addr = ''
        self.receive()

    def send(self, ev=None):
        message = self.chatn.get()
        ChatThread(self.send_s, (message, self.addr)).start()
        self.chats.insert('end', '[%s]:to %s\n' % (ctime(), self.addr))
        self.chats.insert('end', '%s' % message)
        self.chatn.delete(first=0, last=len(message)+1)

    def receive(self):
        ChatThread(self.receive_s, ()).start()

    def send_s(self, message):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.sendto(message, self.addr)

    def receive_s(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(ADDR)
        sock.listen(5)
        cli_sock, self.addr = sock.accept()
        print('addr', self.addr)
        self.chats.insert('end', '%s 上线' % str(self.addr))
        self.top.update()
        while True:
            self.receiveData, self.addr = cli_sock.recvfrom(BUFSIZ)
            print('接受到消息', self.receiveData.decode('utf-8'))
            self.chats.insert('end', '[%s]:from %s' % (ctime(), self.addr))
            self.chats.insert('end', '%s' % self.receiveData.decode('utf-8'))
            self.top.update()


def main():
    s = ChatS()
    tkinter.mainloop()


if __name__ == '__main__':
    main()