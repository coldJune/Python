#!usr/bin/python3
# -*- coding:UTF-8 -*-

import _thread
from time import ctime, sleep

loops = [4, 2]


def loop(nloop, sec, lock):
    # nloop: 第几个线程
    # sec: 时间
    # lock: 分配的锁
    print('start loop', nloop, 'at:', ctime())
    sleep(sec)
    print('loop', nloop, 'done at:', ctime())
    # 当时间到了的时候释放锁
    lock.release()


def main():
    print('starting at:', ctime())
    locks = []
    nloops = range(len(loops))

    for i in nloops:
        # 生成锁对象

        # 通过allocate_lock()函数得到锁对象
        # 通过acquire()取到每个锁
        # 添加进locks列表
        lock = _thread.allocate_lock()
        lock.acquire()
        locks.append(lock)

    for i in nloops:
        # 派生线程

        # 传递循环号，时间、锁对象
        _thread.start_new_thread(loop, (i, loops[i], locks[i]))

    for i in nloops:
        # 等待所有线程的锁都释放完了才执行主线程
        while locks[i].locked():
            pass

    print('all DONE at:', ctime())

if __name__ == '__main__':
    main()
