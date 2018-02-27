#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import threading
from time import ctime, sleep
loops = [4, 2]


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        # 必须先调用基类的构造函数
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def get_result(self):
        return self.res

    def run(self):
        # 必须重写run()方法
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
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        # 等待所有线程
        threads[i].join()

    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()
