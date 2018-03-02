#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# 使用SQLObject代替SQLAlchemy
# 其余和使用SQLAlchemy的相同
from os.path import dirname
from random import randrange as rand
from sqlobject import *
from ushuffleDB import  DBNAME, NAMELEN, \
    randName, FIELDS, tformat, cformat, setup

DSNs = {
    'mysql': 'mysql://root:root@127.0.0.1:3306/%s' % DBNAME,
    'sqlite': 'sqlite:///:memory:',
}


class Users(SQLObject):
    # 扩展了SQLObject.SQLObject类
    # 定义列
    login = StringCol(length=NAMELEN)
    userid = IntCol()
    projid = IntCol()

    def __str__(self):
        # 提供用于显示输出的方法
        return ''.join(map(tformat, (
            self.login, self.userid, self.projid)))


class SQLObjectTest(object):
    def __init__(self, dsn):
        # 确保得到一个可用的数据库，然后返回连接
        try:
            cxn = connectionForURI(dsn)
        except ImportError:
            raise RuntimeError()

        try:
            # 尝试对已存在的表建立连接
            # 规避RMBMS适配器不可用，服务器不在线及数据库不存在等异常
            cxn.releaseConnection(cxn.getConnection())
        except dberrors.OperationalError:
            # 出现异常则创建表
            cxn = connectionForURI(dirname(dsn))
            cxn.query('CREATE DATABASE %s' % DBNAME)
            cxn = connectionForURI(dsn)
        # 成功后在self.cxn中保存连接对象
        self.cxn = sqlhub.processConnection = cxn

    def insert(self):
        # 插入
        for who, userid in randName():
            Users(login=who, userid=userid, projid=rand(1, 5))

    def update(self):
        # 更新
        fr = rand(1, 5)
        to = rand(1, 5)
        i = -1
        users = Users.selectBy(projid=fr)
        for i, user in enumerate(users):
            user.projid = to
        return fr, to, i+1

    def delete(self):
        # 删除
        rm = rand(1, 5)
        users = Users.selectBy(projid=rm)
        i = -1
        for i, user in enumerate(users):
            user.destroySelf()
        return rm, i+1

    def dbDump(self):
        print('\n%s' % ''.join(map(cformat, FIELDS)))
        for user in Users.select():
            print(user)

    def finish(self):
        # 关闭连接
        self.cxn.close()


def main():
    print('***Connect to %r database' % DBNAME)
    db = setup()
    if db not in DSNs:
        print('\nError: %r not support' % db)
        return

    try:
        orm = SQLObjectTest(DSNs[db])
    except RuntimeError:
        print('\nError: %r not support' % db)
        return

    print('\n***Create users table(drop old one if appl.)')
    Users.dropTable(True)
    Users.createTable()

    print('\n*** Insert names into table')
    orm.insert()
    orm.dbDump()

    print('\n*** Move users to a random group')
    fr, to, num = orm.update()
    print('\t(%d users moved) from (%d) to (%d)' % (num, fr, to))
    orm.dbDump()

    print('\n*** Randomly delete group')
    rm, num = orm.delete()
    print('\t(group #%d;%d users removed)' % (rm, num))
    orm.dbDump()

    print('\n*** Drop users table')
    # 使用dropTable()方法
    Users.dropTable()
    print('\n***Close cxns')
    orm.finish()

if __name__ == '__main__':
    main()