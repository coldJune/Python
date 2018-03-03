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
        self.send_sock = None
        self.addr = ''
        self.receive()

    def send(self, ev=None):
        message = self.chatn.get()
        ChatThread(self.send_s, (message,)).start()
        self.chats.insert('end', '[%s]:to %s\n' % (ctime(), self.addr))
        self.chats.insert('end', '%s' % message)
        self.chatn.delete(first=0, last=len(message)+1)

    def receive(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(ADDR)
        sock.listen(5)
        cli_sock, addr = sock.accept()
        self.addr = addr
        self.send_sock = cli_sock
        print('addr', addr)
        self.chats.insert('end', '%s 上线' % str(addr))
        self.top.update()
        ChatThread(self.receive_s, (cli_sock, addr)).start()

    def send_s(self, message):
        self.send_sock.send(bytes(message, 'utf-8'))

    def receive_s(self, cli_sock, addr):
        while True:
            receiveData = cli_sock.recv(BUFSIZ)
            print('接受到消息', receiveData.decode('utf-8'))
            self.chats.insert('end', '[%s]:from %s' % (ctime(), addr))
            self.chats.insert('end', '%s' % receiveData.decode('utf-8'))
            self.top.update()


def main():
    s = ChatS()
    tkinter.mainloop()


if __name__ == '__main__':
    main()