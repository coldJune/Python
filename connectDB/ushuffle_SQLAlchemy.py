#!/usr/bin/python3
# -*- coding:UTF-8 -*-

# 首先导入标准库中的模块(os.path、random)
# 然后是第三方或外部模块(sqlalchemy)
# 最后是应用的本地模块(ushuffleDB)
from os.path import dirname
from random import randrange as rand
from sqlalchemy import Column, Integer, \
    String, create_engine, exc, orm
from sqlalchemy.ext.declarative \
    import declarative_base
from ushuffleDB import DBNAME, NAMELEN, \
    randName, FIELDS, tformat, cformat, setup

# 数据库类型+数据库驱动名称://用户名:密码@地址:端口号/数据库名称
DSNs = {
    'mysql': 'mysql+pymysql://root:root@localhost:3306/%s' % DBNAME,
    'sqlite': 'sqlite:///:memory:',
}

# 使用SQLAlchemy的声明层
# 使用导入的sqlalchemy.ext.declarative.declarative_base
# 创建一个Base类
Base = declarative_base()


class Users(Base):
    # 数据子类
    # __tablename__定义了映射的数据库表名
    __tablename__ = 'users'
    # 列的属性，可以查阅文档来获取所有支持的数据类型
    login = Column(String(NAMELEN))
    userid = Column(Integer, primary_key=True)
    projid = Column(Integer)

    def __str__(self):
        # 用于返回易于阅读的数据行的字符串格式
        return ''.join(map(tformat, (self.login, self.userid, self.projid)))


class SQLAlchemyTest(object):
    def __init__(self, dsn):
        # 类的初始化执行了所有可能的操作以便得到一个可用的数据库，然后保存其连接
        # 通过设置echo参数查看ORM生成的SQL语句
        # create_engine('sqlite:///:memory:', echo=True)
        try:
            eng = create_engine(dsn)
        except ImportError:
            raise RuntimeError()

        try:
            eng.connect()
        except exc.OperationalError:
            # 此处连接失败是因为数据库不存在造成的
            # 使用dirname()来截取掉数据库名，并保留DSN中的剩余部分
            # 使数据库的连接可以正常运行
            # 这是一个典型的操作任务而不是面向应用的任务，所以使用原生SQL
            eng = create_engine(dirname(dsn))
            eng.execute('CREATE DATABASE %s' % DBNAME).close()
            eng = create_engine(dsn)
        # 创建一个会话对象，用于管理单独的事务对象
        # 当涉及一个或多个数据库操作时，可以保证所有要写入的数据都必须提交
        # 然后将这个会话对象保存，并将用户的表和引擎作为实例属性一同保存下来
        # 引擎和表的元数据进行了额外的绑定，使这张表的所有操作都会绑定到这个指定的引擎中
        Session = orm.sessionmaker(bind=eng)
        self.ses = Session()
        self.users = Users.__table__
        self.eng = self.users.metadata.bind = eng

    def insert(self):
        # session.add_all()使用迭代的方式产生一系列的插入操作
        self.ses.add_all(
            Users(login=who, userid=userid, projid=rand(1, 5))
            for who, userid in randName()
        )
        # 决定是提交还是回滚
        self.ses.commit()

    def update(self):
        fr = rand(1, 5)
        to = rand(1, 5)
        i = -1
        # 会话查询的功能，使用query.filter_by()方法进行查找
        users = self.ses.query(Users).filter_by(projid=fr).all()
        for i, user in enumerate(users):
            user.projid = to
        self.ses.commit()
        return fr, to, i+1

    def delete(self):
        rm = rand(1, 5)
        i = -1
        users = self.ses.query(Users).filter_by(projid=rm).all()
        for i, user in enumerate(users):
            self.ses.delete(user)
        self.ses.commit()
        return rm, i+1

    def dbDump(self):
        # 在屏幕上显示正确的输出
        print('\n%s' % ''.join(map(cformat, FIELDS)))
        users = self.ses.query(Users).all()
        for user in users:
            print(user)
        self.ses.commit()

    def __getattr__(self, attr):
        # __getattr__()可以避开创建drop()和create()方法
        # __getattr__()只有在属性查找失败时才会被调用
        # 当调用orm.drop()并发现没有这个方法时，就会调用getattr(orm, 'drop')
        # 此时调用__getattr__()，并且将属性名委托给self.users。结束期会发现
        # slef.users存在一个drop属性，然后传递这个方法调用到self.users.drop()中
        return getattr(self.users, attr)

    def finish(self):
        # 关闭连接
        self.ses.connection().close()


def main():
    # 入口函数
    print('\n***Connnect to %r database' % DBNAME)
    db = setup()
    if db not in DSNs:
        print('ERROR: %r not supported, exit' % db)
        return

    try:
        orm = SQLAlchemyTest(DSNs[db])
    except RuntimeError:
        print('ERROR: %r not supported, exit' % db)
        return

    print('\n*** Create users table(drop old one if appl.')
    orm.drop(checkfirst=True)
    orm.create()

    print('\n***Insert namse into table')
    orm.insert()
    orm.dbDump()

    print('\n***Move users to a random group')
    fr, to, num = orm.update()
    print('\t(%d users moved) from (%d) to (%d))' % (num, fr, to))
    orm.dbDump()

    print('\n***Randomly delete group')
    rm, num = orm.delete()
    print('\t(group #%d; %d users removed)' % (rm, num))
    orm.dbDump()

    print('\n***Drop users table')
    orm.drop()
    print('***Close cxns')
    orm.finish()

if __name__ == '__main__':
    main()