#coding:gbk
'''
Created on 2017年1月9日

@author: coldJune
'''
import uuid,pymysql

def createActivationCode(num,length=16):
    result=[]
    while num>0:
        temp=str(uuid.uuid1()).replace('-','')[:length]
        tmp=[]
        for n in range(length):
            if n%4==0:
                tmp.append(temp[n:n+4])
        temp='-'.join(tmp)
        if temp[-1]=='-':
            temp=str(temp[:-1])
        num-=1
        if temp not in result:
            result.append(temp)
    return result

def saveToMySQL(activationCodes):
    #连接数据库
    connect=pymysql.connect(host='localhost',port=3306,user='root',password='root',db='python')
    cur=connect.cursor()
    cur.execute("create table if not exists act_code(id int auto_increment primary key,code varchar(255))")
        
    for n in range(len(activationCodes)):
        sql="INSERT INTO ACT_CODE(CODE) VALUES('%s');" %(activationCodes[n])
        
        cur.execute(sql)
    connect.commit()
    cur.close()
    connect.close()


activationCodes=createActivationCode(5, 16)
print(activationCodes)
saveToMySQL(activationCodes)
