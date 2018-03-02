#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# 主要导入的是MongoClient对象和及其包异常errors
from random import randrange as rand
from pymongo import MongoClient, errors
from ushuffleDB import DBNAME, randName, FIELDS, tformat, cformat

# 设置了集合(“表”)名
COLLECTION = 'users'


class MongoTest(object):
    def __init__(self):
        # 创建一个连接，如果服务器不可达，则抛出异常
        try:
            cxn = MongoClient()
        except errors.AutoReconnect:
            raise RuntimeError
        # 创建并复用数据库及“users”集合
        # 关系数据库中的表会对列的格式进行定义，
        # 然后使遵循这个列定义的每条记录成为一行
        # 非关系数据库中集合没有任何模式的需求，
        # 每条记录都有其特定的文档
        # 每条记录都定义了自己的模式，所以保存的任何记录都会写入集合中
        self.db = cxn[DBNAME]
        self.users = self.db[COLLECTION]

    def insert(self):
        # 向MongoDB的集合中添加值
        # 使用dict()工厂函数为每条记录创建一个文档
        # 然后将所有文档通过生成器表达式的方式传递给集合的insert()方法
        self.users.insert(
            dict(login=who, userid=uid, projid=rand(1, 5)
                 )for who, uid in randName()
        )

    def update(self):
        # 集合的update()方法可以给开发者相比于典型的数据库系统更多的选项
        fr = rand(1, 5)
        to = rand(1, 5)
        i = -1
        # 在更新前，首先查询系统中的项目ID(projid)与要更新的项目组相匹配的所有用户
        # 使用find()方法，并将查询条件传进去(类似SQL的SELECT语句)
        for i, user in enumerate(self.users.find({'projid': fr})):
            # 使用$set指令可以显式地修改已存在的值
            # 每条MongoDB指令都代表一个修改操作，使得修改操作更加高效、有用和便捷
            # 除了$set还有一些操作可以用于递增字段值、删除字段(键-值对)、对数组添加/删除值
            # update()方法可以用来修改多个文档(将multi标志设为True)
            self.users.update(user, {
                '$set': {'projid': to}
            })
        return fr, to, i+1

    def delete(self):
        # 当得到所有匹配查询的用户后，一次性对其执行remove()操作进行删除
        # 然后返回结果
        rm = rand(1, 5)
        i = -1
        for i, user in enumerate(self.users.find({'projid': rm})):
            self.users.remove(user)
        return rm, i+1

    def dbDump(self):
        # 没有天剑会返回集合中所有用户并对数据进行字符串格式化向用户显示
        print('%s' % ''.join(map(cformat, FIELDS)))
        for user in self.users.find():
            print(''.join(map(tformat, (
                user[k] for k in FIELDS))))


def main():
    print('***Connect to %r database' % DBNAME)
    try:
        mongo = MongoTest()
    except RuntimeError:
        print('\nERROR: MongoDB server unreadable, exit')
        return

    print('\n***Insert names into table')
    mongo.insert()
    mongo.dbDump()

    print('\n***Move users to a random group')
    fr, to, num = mongo.update()
    print('\t(%d users moved) from (%d) to (%d)' % (num, fr, to))
    mongo.dbDump()

    print('\n*** Randomly delete group')
    rm, num = mongo.delete()
    print('\tgroup #%d; %d users removed' % (rm, num))
    mongo.dbDump()

    print('\n***Drop users table')
    mongo.db.drop_collection(COLLECTION)

if __name__ == '__main__':
    main()
