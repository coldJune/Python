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
    # 服务器的实现类，继承自ChatWindowBase
    def __init__(self):
        # 调用父类的__init__()方法
        super(ChatS, self).__init__()
        self.label.configure(text='服务器')
        # 设置属性
        # 用于保存客户端链接对象
        # 用于保存客户端链接地址
        self.send_sock = None
        self.addr = ''
        # 在服务器窗口创建时调用
        self.receive()

    def send(self, ev=None):
        # 获取输入框信息
        message = self.chatn.get()
        # 启动线程
        ChatThread(self.send_s, (message,)).start()
        # 将输入框信息按照格式显示在Listbox
        self.chats.insert('end', '[%s]:to %s\n' % (ctime(), self.addr))
        self.chats.insert('end', '%s' % message)
        # 删除输入框内容
        self.chatn.delete(first=0, last=len(message)+1)

    def receive(self):
        # 创建socket链接
        # 绑定地址
        # 设置监听
        # 阻塞直到有链接调用，然后保存链接的客户端对象和地址
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(ADDR)
        sock.listen(5)
        cli_sock, addr = sock.accept()
        self.addr = addr
        self.send_sock = cli_sock
        print('addr', addr)
        # 有链接接入时在Listbox中显示消息
        self.chats.insert('end', '%s 上线' % str(addr))
        # 更新顶层窗口
        self.top.update()
        # 启动接受消息的线程
        ChatThread(self.receive_s, (cli_sock, addr)).start()

    def send_s(self, message):
        # 向客户端发送消息
        self.send_sock.send(bytes(message, 'utf-8'))

    def receive_s(self, cli_sock, addr):
        # 接受消息
        # cli_sock: 客户端sock
        # addr: 客户端地址
        while True:
            # 进入无限循环接受消息，并在Listbox显示消息
            receiveData = cli_sock.recv(BUFSIZ)
            print('接受到消息', receiveData.decode('utf-8'))
            self.chats.insert('end', '[%s]:from %s' % (ctime(), addr))
            self.chats.insert('end', '%s' % receiveData.decode('utf-8'))
            self.top.update()


def main():
    # 创建服务器窗口
    s = ChatS()
    # 调用mainloop()运行整个GUI
    tkinter.mainloop()


if __name__ == '__main__':
    main()