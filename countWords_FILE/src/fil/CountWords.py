#coding:gbk
'''
Created on 2017年1月10日

@author: coldjune
'''
from itertools import count


file_name='./../../txt/movie.txt'


#计算字数
def countWords(file_name):
    all_word=[]
    #打开文件
    with open(file_name, 'r') as f:
        lines_count=0
        words_count=0
        character_count=0
        for line in f:
            words=line.split()
            lines_count+=1
            words_count+=len(words)
            character_count+=len(line)
            all_word.extend(words)
        print (lines_count)
        print(words_count)
        print(character_count)
    return all_word
#计算频率
def countRate(words):
    words_rate={}
    for word in words:
        #单词开始和结束去除非法字符
        if not word[0].isalpha():
            word=word[1:]
        if len(word)>=2 and not word[-1].isalpha():
            word=word[:-1]
        if word!='':
            if word in words_rate:
                words_rate[word]+=1
            else:
                words_rate[word]=1
    return words_rate

words=countWords(file_name)
rateWords=countRate(words)
for key in rateWords:
    print("%s:%d" %(key,rateWords[key]))
