#coding:utf-8
'''
Created on 2017年1月19日

@author: coldJune
'''
import urllib.request,socket,re,sys,os

#文件保存路径
imgPath = "./../imgPath"

#保存文件
def saveImg(path):
    if not os.path.isdir(imgPath):
        os.mkdir(imgPath)
        
    #设置每个图片路径
    pos=path.rindex('/')
    t=os.path.join(imgPath,path[pos+1:])
    return t

def catchImg():
    url="https://www.douban.com"
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7'}
    req=urllib.request.Request(url=url,headers=headers)
    res=urllib.request.urlopen(req)
    data=res.read()
    for link,t in set(re.findall(r'(https:[^s]*?(jpg|png|git))',str(data))):
        print(link)
        try:
            urllib.request.urlretrieve(link,saveImg(link))
        except:
            print('失败')
            
if __name__=='__main__':
    catchImg()