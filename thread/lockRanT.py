#!/usr/bin/python3
# -*- coding:UTF-8 -*-

from atexit import  register
from random import randrange
from threading import Thread, Lock, current_thread
from time import sleep, ctime


class CleanOutputSet(set):
    # 集合的子类，将默认输出改变为将其所有元素
    # 按照逗号分隔的字符串
    def __str__(self):
        return ', '.join(x for x in self)


# 锁
# 随机数量的线程(3~6)，每个线程暂停或睡眠2~4秒
lock = Lock()
loops = (randrange(2, 5) for x in range(randrange(3, 7)))
remaining = CleanOutputSet()


def loop(sec):
    # 获取当前执行的线程名，然后获取锁并保存线程名
    myname = current_thread().name
    lock.acquire()
    remaining.add(myname)
    print('[%s] Started %s' % (ctime(), myname))
    # 释放锁并睡眠随机秒
    lock.release()
    sleep(sec)
    # 重新获取锁，输出后再释放锁
    lock.acquire()
    remaining.remove(myname)
    print('[%s] Completed %s (%d sec)' % (ctime(), myname, sec))
    print('     (remaining: %s)' % (remaining or 'NONE'))
    lock.release()


def _main():
    for pause in loops:
        Thread(target=loop, args=(pause,)).start()


@register
def _atexit():
    print('all DONE at:', ctime())


if __name__ == '__main__':
    _main()
