#!/usr/bin/python
# -*- coding:UTF-8 -*-

import threading
from time import ctime, sleep

loops = [4, 2]


def loop(nloop, sec):
    print('start loop', nloop, 'at:', ctime())
    sleep(sec)
    print('loop', nloop, 'done at:', ctime())


def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)

    for i in nloops:
        # 启动线程
        threads[i].start()

    for i in nloops:
        # 等待所有线程结束
        threads[i].join()

    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()
