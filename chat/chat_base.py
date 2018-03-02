#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import tkinter as tk


class ChatWindowBase(object):
    def __init__(self):
        self.top = tk.Tk()
        self.label = tk.Label(self.top, text='聊天室')
        self.label.pack()

        self.chatfm = tk.Frame(self.top)
        self.chatsb = tk.Scrollbar(self.chatfm)
        self.chatsb.pack(side='right', fill='y')
        self.chats = tk.Listbox(self.chatfm, height=15, width=50, yscrollcommand=self.chatsb.set)
        self.chatsb.config(command=self.chats.yview())
        self.chats.pack(side='left', fill='both')
        self.chatfm.pack()

        self.sendfm = tk.Frame(self.top, width=50)
        self.chatn = tk.Entry(self.sendfm, width=40)
        self.chatn .bind('<Return>', self.send)
        self.chatn.pack(side='left')
        self.sendchat = tk.Button(self.sendfm, text='发送', command=self.send)
        self.sendchat.pack(side='right', fill='both')
        self.sendfm.pack()

    def send(self):
        pass

    def receive(self):
        pass



