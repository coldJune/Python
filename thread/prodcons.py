#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# 使用queue.Queue对象和之前的myThread.MyThread线程类
from random import randint
from time import sleep
from queue import Queue
from myThread import MyThread


def writeQ(queue):
    # 将一个对象放入队列中
    print('producing object for Q...')
    queue.put('xxx', 1)
    print('size now', queue.qsize())


def readQ(queue):
    # 消费队列中的一个对象
    val = queue.get(1)
    print('consumed object from Q... size now', queue.qsize())


def writer(queue, loops):
    # 作为单个线程运行
    # 向队列中放入一个对象，等待片刻，然后重复上述步骤
    # 直至达到脚本执行时随机生成的次数没值
    for i in range(loops):
        writeQ(queue)
        # 睡眠的随机秒数比reader短是为了阻碍reader从空队列中获取对象
        sleep(randint(1, 3))


def reader(queue, loops):
    # 作为单个线程运行
    # 消耗队列中一个对象，等待片刻，然后重复上述步骤
    # 直至达到脚本执行时随机生成的次数没值
    for i in range(loops):
        readQ(queue)
        sleep(randint(2, 5))

# 设置派生和执行的线程总数
funcs = [writer, reader]
nfuncs = range(len(funcs))


def main():
    nloops = randint(2, 5)
    q = Queue(32)
    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print('all DONE')

if __name__ == '__main__':
    main()
