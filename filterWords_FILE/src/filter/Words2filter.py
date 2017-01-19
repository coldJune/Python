#coding:utf-8
'''
Created on 2017年1月19日

@author:coldJune
'''
from nltk.compat import raw_input
def words2filter():
    #打开文件读取敏感词汇
    with open("./../../words/words.txt","r") as file:
        words=file.read().split()
        print(words)
    
    user_input=raw_input("Please input a word:")
    for word in words:
        if word in user_input:
            user_input=user_input.replace(str(word), "*"*len(word))
    
    print (user_input)
    return

if __name__=='__main__':
    words2filter()