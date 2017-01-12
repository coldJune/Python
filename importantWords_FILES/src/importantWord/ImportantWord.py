#coding:utf-8
'''
Created on 2017��1��12��

@author: coldJune
'''
import re,os
from audioop import reverse

#取得文件夹下所有txt文件
def get_files(path):
    filepath=os.listdir(path)
    files=[]
    for fp in filepath:
        fppath=path+'/'+fp
        if(os.path.isfile(fppath)):
            files.append(fppath)
        elif(os.path.isdir(fppath)):
            files+=get_files(fppath)
    return files

#取得文件中的重要词汇
def get_important_word(files):
    worddict={}
    for filename in files:
        with open(filename,'r',encoding='utf-8') as f:
            s=f.read()
            words=s.split()
            # words=filter(lambda words:'我，还是过于单纯' not in words,words)
            # words=re.findall(r'[a-zA-Z0-9+]',s)
            for word in words:
                worddict[word]=worddict[word]+1 if word in worddict else 1
    #字典排序
    #e表示items中一个元素，e[1]表示按值排序，e[0]表示按键排序
    wordsort=sorted(worddict.items(),key=lambda e:e[1],reverse=True)     
    return wordsort

if __name__=='__main__':
    files=get_files('./../../txts')
    print(files)
    wordsort=get_important_word(files)
    if wordsort==[]:
        print("文件为空")
    else:
        #避免遗漏多个最大值
        maxnum=1
        for i in range(len(wordsort)-1):
            if wordsort[i][1]==wordsort[i+1][1]:
                maxnum+=1
            else:
                break
        for i in range(maxnum):
            print(wordsort[i])