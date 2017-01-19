#coding:utf-8
'''
Created on 2017年1月19日

@author: coldjune
'''
from nltk.compat import raw_input
def filterWords():
    with open("./../../words/words.txt") as f:
        words=f.read().split()
        print(words)
    
    user_input=raw_input("Please input a word:")
    #标识是否为敏感词汇
    flag=True
    for word in words:
        if word in user_input:
            flag=True
            break
        else:
            flag=False
    if flag:
        print("Freedom")
    else:
        print("Human Rights")
    return

if __name__=="__main__":
    filterWords()