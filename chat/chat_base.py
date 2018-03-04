#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import tkinter as tk


class ChatWindowBase(object):
    # 窗口的基类，创建通用的窗口布局
    def __init__(self):
        # 初始化方法
        # 创建tkinter.TK()顶层窗口
        # 所有主要控件都是构建在顶层窗口对象之上
        # 通过tkinter.TK()创建
        self.top = tk.Tk()
        # 在顶层窗口上添加Label控件
        self.label = tk.Label(self.top, text='聊天室')
        # 通过Packer来管理和显示控件
        # 调用pack()方法显示布局
        self.label.pack()

        # 通过Frame控件创建子容器，用于存放其他控件
        # 该对象将作为单个子对象代替父对象
        self.chatfm = tk.Frame(self.top)
        # Scrollbar可以让显示的数据在超过Listbox的大小时能够移动列表
        self.chatsb = tk.Scrollbar(self.chatfm)
        # 将Scrollbar放置在子容器的右侧，并且是针对y轴
        self.chatsb.pack(side='right', fill='y')
        # 在子容器中创建高为15宽为50的Listbox
        # 将Listbox和Scrollbar关联起来
        # 显示列表
        # 显示子容器
        # 控件的显示应该内部控件先显示，再显示外部控件
        self.chats = tk.Listbox(self.chatfm, height=15,
                                width=50, yscrollcommand=self.chatsb.set)
        self.chatsb.config(command=self.chats.yview())
        self.chats.pack(side='left', fill='both')
        self.chatfm.pack()

        # 创建发送消息的子容器
        self.sendfm = tk.Frame(self.top, width=50)
        # 创建输入框
        # 绑定回车键，并且绑定send方法
        # 绑定一个方法是指在触发一个事件时会去调用的方法
        self.chatn = tk.Entry(self.sendfm, width=40)
        self.chatn.bind('<Return>', self.send)
        self.chatn.pack(side='left')
        # 添加按钮控件、绑定方法
        self.sendchat = tk.Button(self.sendfm, text='发送', command=self.send)
        self.sendchat.pack(side='right', fill='both')
        self.sendfm.pack()

    def send(self, ev=None):
        # 创建发送消息的方法
        # 空实现是为了继承时扩展
        pass

    def receive(self):
        # 创建接受消息的方法
        # 空实现是为了继承时扩展
        pass



