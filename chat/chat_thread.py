#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import threading


class ChatThread(threading.Thread):
    # 继承自threading.Thread，用于创建聊天室的通用线程
    def __init__(self, func, args):
        # func: 方法
        # args：方法所需要的参数
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        # 实现run方法，将参数传给相应的方法
        self.func(*self.args)
