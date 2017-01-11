#coding:gbk
'''
Created on 2017年1月11日

@author: coldJune
'''

from PIL import Image
import os
#输入文件路径
inputPath='./../../beforeImage/'
#输出文件路径
outputPath='./../../afterImage/'

'''
    inputPath是输入目录
    outputPath是输出目录
    file_name是文件名
    imgtype是文件类型
'''

def processImage(inputresource,outputresource,file_name,imgtype):
    imgtype='jpeg' if imgtype=='jpg' else 'png'
    #打开图片
    im=Image.open("r"+inputresource+file_name)
    
    #缩放比例
    rate=max(im.size[0]/640.0 if im.size[0]>640 else 0,im.size[1]/1136.0 if im.size[1]>1136 else 0)
    
    if rate:
        im.thumbnail((im.size[0]/rate,im.size[1]/rate))
    im.save("r"+outputresource+file_name,imgtype)


def run():
    #切换到源目录，遍历源目录下所有图片
    os.chdir(inputPath)
    for i  in os.listdir(os.getcwd()):
        #检查后缀
        postfix=os.path.splitext(i)[1]
        if postfix == '.jpg' or postfix == '.png':
            processImage(inputPath, outputPath,i, postfix)
            

if __name__=='__main__':
    run()