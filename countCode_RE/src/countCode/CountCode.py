#coding:utf-8
'''
Created on 2017��1��16��

@author: coldJune
'''
import os,sys,re

def getFile(path):
    filepath=os.listdir(path)
    javas=[]
    for fp in filepath:
        fppath=path+'/'+fp
        if os.path.isfile(fppath) and fppath[-5:]=='.java':
            javas.append(fppath)
        elif os.path.isdir(fppath):
            javas+=getFile(fppath)
    return javas

def countNum(files):
    Num={}
    for file in files:
        with open(file,'r',encoding='gbk') as fi:
            cols=fi.readlines()
            for col in range(len(cols)):
                count=1
                if '//' in cols[col]:
                    
                    Num['comment']= Num['comment']+1 if 'comment' in Num else 1 
                elif '/*' in cols[col] or '/**' in cols[col]:
                    while '*/' not in cols[col]:
                        count+=1
                        col+=1
                    Num['comment']=Num['comment']+count if 'comment' in Num else count
                elif cols[col].isspace():
                    Num['space']=Num['space']+1 if 'space' in Num else 1
                else:
                    Num['code']=Num['code']+1 if 'code' in Num else 1

    return Num

if __name__=="__main__":
    path=sys.argv[1]
    files=getFile(path)
    Num=countNum(files)
    print(Num)