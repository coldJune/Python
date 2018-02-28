#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# 导入必需的模块
import os
from random import randrange as rand

# 创建了全局变量
# 用于显示列的大小，以及支持的数据库种类
COLSIZ = 10
FIELDS = ('login', 'userid', 'projid')
RDBMSs = {
    's': 'sqlite',
    'm': 'mysql',
}
DBNAME = 'test'
DBUSER = 'root'
# 数据库异常变量，根据用户选择运行的数据库系统的不同来制定数据库异常模块
DB_EXC = None
NAMELEN = 16

# 格式化字符串以显示标题
# 全大写格式化函数，接收每个列名并使用str.upper()方法把它转换为头部的全大写形式
# 两个函数都将其输出左对齐，并限制为10个字符的宽度ljust(COLSIZ)
tformat = lambda s: str(s).title().ljust(COLSIZ)
cformat = lambda s: s.upper().ljust(COLSIZ)


def setup():
    return RDBMSs[input('''
        Choose a database system:
        (M)ySQL
        (S)QLite
        Enter choice:
    ''').strip().lower()[0]]


def connect(db):
    # 数据库一致性访问的核心
    # 在每部分的开始出尝试加载对应的数据库模块，如果没有找到合适的模块
    # 就返回None，表示无法支持数据库系统
    global DB_EXC
    dbDir = '%s_%s' % (db, DBNAME)

    if db == 'sqlite':
        try:
            # 尝试加载sqlite3模块
            import sqlite3
        except ImportError:
            return None
        DB_EXC = sqlite3
        # 当对SQLite调用connect()时，会使用已存在的目录
        # 如果没有，则创建一个新目录
        if not os.path.isdir(dbDir):
            os.mkdir(dbDir)
        cxn = sqlite3.connect(os.path.join(dbDir, DBNAME))
    elif db == 'mysql':
        try:
            # 由于MySQLdb不支持python3.6，所以导入pymysql
            import pymysql
            import pymysql.err as DB_EXC
            try:
                cxn = pymysql.connect(host="localhost",
                                      user="root",
                                      password="root",
                                      port=3306,
                                      db=DBNAME)
            except DB_EXC.InternalError:
                try:
                    cxn = pymysql.connect(host="localhost",
                                          user="root",
                                          password="root",
                                          port=3306)
                    cxn.query('CREATE DATABASE %s' % DBNAME)
                    cxn.commit()
                    cxn.close()
                    cxn = pymysql.connect(host="localhost",
                                          user="root",
                                          password="root",
                                          port=3306,
                                          db=DBNAME)
                except DB_EXC.InternalError:
                    return None
        except ImportError:
            return None
    else:
        return None
    return cxn


def create(cur):
    # 创建一个新表users
    try:
        cur.execute('''
            CREATE  TABLE  users(
                login VARCHAR(%d),
                userid INTEGER,
                projid INTEGER
            )
        ''' % NAMELEN)
    except DB_EXC.InternalError as e:
        # 如果发生错误，几乎总是这个表已经存在了
        # 删除该表，重新创建
        drop(cur)
        create(cur)

# 删除数据库表的函数
drop = lambda cur: cur.execute('DROP TABLE users')

# 由用户名和用户ID组成的常量
NAMES = (
    ('bob', 1234), ('angela', 4567), ('dave', 4523)
)


def randName():
    # 生成器
    pick = set(NAMES)
    while pick:
        yield pick.pop()


def insert(cur, db):
    # 插入函数
    # SQLite风格是qmark参数风格，而MySQL使用的是format参数风格
    # 对于每个用户名-用户ID对，都会被分配到一个项目卒中。
    # 项目ID从四个不同的组中随机选出的
    if db == 'sqlite':
        cur.executemany("INSERT INTO users VALUES(?,?,?)",
                        [(who, uid, rand(1, 5)) for who, uid in randName()])
    elif db == 'mysql':
        cur.executemany("INSERT INTO users VALUES(%s, %s, %s)",
                        [(who, uid, rand(1, 5)) for who, uid in randName()])

# 返回最后一次操作后影响的行数，如果游标对象不支持该属性，则返回-1
getRC = lambda cur: cur.rowcount if hasattr(cur, 'rowcount') else -1


# update()和delete()函数会随机选择项目组中的成员
# 更新操作会将其从当前组移动到另一个随机选择的组中
# 删除操作会将该组的成员全部删除
def update(cur):
    fr = rand(1, 5)
    to = rand(1, 5)
    cur.execute('UPDATE users SET projid=%d WHERE projid=%d' % (to, fr))
    return fr, to, getRC(cur)


def delete(cur):
    rm = rand(1, 5)
    cur.execute('DELETE FROM users WHERE projid=%d' % rm)
    return rm, getRC(cur)


def dbDump(cur):
    # 来去所有行，将其按照打印格式进行格式化，然后显示
    cur.execute('SELECT * FROM users')
    # 格式化标题
    print('%s' % ''.join(map(cformat, FIELDS)))
    for data in cur.fetchall():
        # 将数据(login,userid,projid)通过map()传递给tformat()，
        # 是数据转化为字符串，将其格式化为标题风格
        # 字符串按照COLSIZ的列宽度进行左对齐
        print(''.join(map(tformat, data)))


def main():
    # 主函数
    db = setup()
    print('*** Connect to %r database' % db)
    cxn = connect(db)
    if not cxn:
        print('ERROR: %r not supported or unreadable, exit' % db)
        return
    cur = cxn.cursor()
    print('***Creating users table')
    create(cur=cur)

    print('***Inserting names into table')
    insert(cur, db)
    dbDump(cur)

    print('\n***Randomly moving folks')
    fr, to, num = update(cur)
    print('(%d users moved) from (%d) to (%d)' % (num, fr, to))
    dbDump(cur)

    print('***Randomly choosing group')
    rm, num = delete(cur)
    print('\t(group #%d; %d users removed)' % (rm, num))
    dbDump(cur)

    print('\n***Droping users table')
    drop(cur)
    print('\n*** Close cxns')
    cur.close()
    cxn.commit()
    cxn.close()

if __name__ == '__main__':
    main()
