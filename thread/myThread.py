#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import threading
from time import ctime, sleep


class MyThread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def get_result(self):
        # 返回每一次的执行结果
        return self.res

    def run(self):
        print('starting at:', ctime())
        self.res = self.func(*self.args)
        print('done at:', ctime())
