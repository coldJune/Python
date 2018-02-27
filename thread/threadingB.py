#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import threading
from time import ctime, sleep

loops = [4, 2]


class ThreadFunc(object):
    def __init__(self, func, args, name=''):
        self.name = name
        self.func = func
        self.args = args

    def __call__(self):
        # Thread类的代码将调用ThreadFunc对象，此时会调用这个方法
        # 因为init方法已经设定相关值，所以不需要再将其传递给Thread()的构造函数
        self.func(*self.args)


def loop(nloop, sec):
    print('start loop', nloop, 'at:', ctime())
    sleep(sec)
    print('loop ', nloop, 'done at:', ctime())


def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        # 创建所有线程
        t = threading.Thread(target=ThreadFunc(loop, (i, loops[i])))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        # 等待所有线程
        threads[i].join()

    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()
