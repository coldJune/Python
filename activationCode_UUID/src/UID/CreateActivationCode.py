#coding:gbk
'''
Created on 2017年1月8日

@author: coldjune
'''

import uuid,string

def createActivationCode(num,length=16):
    result=[]
    
    while num>0:
        uuid_id=uuid.uuid1()
        #删除-
        temp=str(uuid_id).replace('-', '')[:length]+'\n'
        #没四位添加一个'-'
        l=len(temp)
        tem=[]
        for n in range(l):
            if n%4==0:
                tem.append(temp[n:n+4])
        temp='-'.join(tem)
        #截取倒数第二字符
        if temp[-2]=='-':
            #截取到倒数第二个字符前，并加上换行符
            temp=temp[:-2]+'\n'
                
        if temp not in result:
            result.append(temp)
        num-=1
    
    activationCode=open('./../../activation/activationCode.txt','w')
    activationCode.writelines(result)
    activationCode.close()

createActivationCode(5,21)