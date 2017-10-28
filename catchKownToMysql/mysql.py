#!/usr/bin/python3
#-*- coding:utf-8 -*-
import time
import pymysql

def Mysql:
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    def __init__(self):
        try:
            self.db = pymysql.connect('localhost','root','root','known')
            self.cur = db.cursor()
        except pymysql.Error as e:
            print(self.getCurrentTime(),"连接数据库错误，原因%d: %s"
                  %(e.args[0],e.args[1]))

    def insertData(self,table,my_dict):
        try:
            cols = ', '.join(my_dict.keys())
            values = '"," '.join(my_dict.values())
            sql = "INSERT INTO %s (%s) VALUES (%s)" %(table,cols,'"'+values+'"')
            try:
                result = self.cur.execute(sql)
                insert_id = self.cur.lastrowid
                self.db.commit()
                if result:
                    return insert_id
                else:
                    return 0
            except pymysql.Error as e:
                self.db.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print(self.getCurrentTime(),"数据已存在，未插入数据")
                else:
                    print(self.getCurrentTime(),"插入数据失败，原因 %d: %s"
                          %(e.args[0],e.args[1]))
        except pymysql.Error as e:
            print(self.getCurrentTime(),'数据库错误，原因%d: %s'
                  %(e.args[0],e.args[1]))
