#!usr/bin/python3
# -*- coding:UTF-8 -*-

import _thread
from time import ctime, sleep


def loop_0():
    print('start loop_0 at:', ctime())
    sleep(4)
    print('loop_0 done at:', ctime())


def loop_1():
    print('start loop_1 at:', ctime())
    sleep(2)
    print('loop_1 done at:', ctime())


def main():
    print('starting at:', ctime())
    # start_new_thread 方法即使要执行的函数不需要参数，也需要传递一个空元组
    _thread.start_new_thread(loop_0, ())
    _thread.start_new_thread(loop_1, ())
    # 阻止主线程的执行，保证其最后执行，后续去掉这种方式，引入锁的方式
    sleep(6)
    print('all done at', ctime())


if __name__ == '__main__':
    main()
