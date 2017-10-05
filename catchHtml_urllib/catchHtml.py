#!/usr/bin/python3

import urllib.request
import os
import urllib.parse

def check_dir2write(dir_name,file_name,data):
    #Discription:For checking is dir existing,if it existed ,do
    #noting,otherwise create a dir.then,write the data to the file
    #
    #Input:dir_name the name of dir
    #
    #Input:file_name the name of file which will be wrote
    #
    #Input:data the data write in file
    #
    #Output:None
    if(not os.path.exists(dir_name)):
        os.mkdir(dir_name)
    
    path=dir_name+"/"+file_name
    with open(path,'wb') as fhandle:
        fhandle.write(data)
        
def readHtml():
    file=urllib.request.urlopen('https://www.baidu.com')
    data=file.read()
    dataline=file.readline()
    check_dir2write('./html','1.html',data) 

def simulate_browser(url,file_name):
    #Discription: simulate browser to access web
    #
    #Input:url 
    #
    #Output:None
    url='https://www.baidu.com'
    header={
        'User-Agent':'''Mozilla/5.0 (Windows NT 10.0; Win64; x64)
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100
        Safari/537.36'''
    }
    request=urllib.request.Request(url,headers=header)
    response=urllib.request.urlopen(request).read()
    check_dir2write('./html',file_name,response)

def simulate_search():
    url='https://www.baidu.com/s?wd='
    key='芒果'
    key_code=urllib.request.quote(key)#因为URL里含中文，需要进行编码
    url_all=url+key_code
    simulate_browser(url_all,'search_result.html') 

