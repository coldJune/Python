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
    # 客户端的实现类，继承子ChatWindowBase方法
    def __init__(self):
        # 初始化方法
        # 在子类中必须调用父类的__init__()方法
        super(ChatC, self).__init__()
        # 设置label的标题
        self.label.configure(text='客户端')
        # 设置属性，用于保存sock对象用于发送和接受消息
        self.sock = None
        # 在创建窗口时链接服务器，
        # 客户端需要比服务器后创建
        # 否则链接会创建失败
        self.receive()

    def send(self, ev=None):
        # 继承自父类，为控件调用的方法
        # 获取输入框的值
        message = self.chatn.get()
        # 创建发送消息的线程
        # 将方法和方法需要的参数用作线程初始化，并启动线程
        ChatThread(self.send_c, (message,)).start()
        # 在Listbox中按格式显示消息
        self.chats.insert('end', '[%s]:to %s' % (ctime(), ADDR))
        self.chats.insert('end', '%s' % message)
        # 删除输入框中的消息
        self.chatn.delete(first=0, last=len(message)+1)
        # 通过更新顶层窗口显示消息
        self.top.update()

    def receive(self):
        # 继承自父类
        # 创建socket链接
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(ADDR)
        # 启动线程
        # 将方法和方法需要的参数用作线程初始化，并启动线程
        ChatThread(self.receive_c, (self.sock,)).start()

    def send_c(self, message):
        # 调用sock的send方法，向服务器发送消息
        self.sock.send(bytes(message, 'utf-8'))

    def receive_c(self, sock):
        # 接受服务器数据的方法
        while True:
            # 进入循环，等待服务器发送的消息
            data = sock.recv(BUFSIZ)
            # 将消息按照格式显示到Listbox中
            self.chats.insert('end', '[%s]:from %s' % (ctime(), ADDR))
            self.chats.insert('end', '%s' % data.decode('utf-8'))
            # 更新控件
            self.top.update()


def main():
    # 实例化客户端窗口
    c = ChatC()
    # 调用mainloop方法运行整个GUI
    tkinter.mainloop()


if __name__ == '__main__':
    main()
