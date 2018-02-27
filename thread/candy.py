#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# 导入相应的模块和信号量类
# BoundedSemaphore的额外功能是这个计数器的值永远不会超过它的初始值
# 它可以防范其中信号量释放次数多余获得次数的异常用例
from atexit import register
from random import randrange
from threading import BoundedSemaphore, Lock, Thread
from time import sleep, ctime

# 全局变量
# 锁
# 库存商品最大值的常量
# 糖果托盘
lock = Lock()
MAX = 5
candytray = BoundedSemaphore(MAX)


def refill():
    # 当虚构的糖果机所有者向库存中添加糖果时执行
    # 代码会输出用户的行动，并在某人添加的糖果超过最大库存是给予警告
    lock.acquire()
    print('Refilling candy...')
    try:
        candytray.release()
    except ValueError:
        print('full, skipping')
    else:
        print('OK')
    lock.release()


def buy():
    # 允许消费者获取一个单位的库存
    lock.acquire()
    print('Buying candy....')
    # 检测是否所有资源都已经消费完了
    # 通过传入非阻塞的标志False，让调用不再阻塞，而在应当阻塞的时候返回一个False
    # 指明没有更多资源
    if candytray.acquire(False):
        print('OK')
    else:
        print('Empty, skipping')
    lock.release()


def producer(loops):
    for i in range(loops):
        refill()
        sleep(randrange(3))


def consumer(loops):
    for i in range(loops):
        buy()
        sleep(randrange(3))


def _main():
    print('starting at:', ctime())
    nloops = randrange(2, 6)
    print('THE CANDY MACHINE (full with %d bars)' % MAX)
    Thread(target=consumer, args=(randrange(nloops, nloops+MAX+2),)).start()
    Thread(target=producer, args=(nloops,)).start()


@register
def _atexit():
    print('all DONE at:', ctime())

if __name__ == '__main__':
    _main()
