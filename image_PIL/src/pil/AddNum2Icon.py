# coding=gbk
'''
Created on 2017锟斤拷1锟斤拷7锟斤拷
@author:
'''
from PIL import Image,ImageDraw,ImageFont

#文件的输入路径和文件输出路径及相应文件名
inputSrc="./../../inputImg/"
outputSrc="./../../outputImg/"
fontSrc="./../../fonts/STXINGKA.TTF"
inputFile="qztmp.jpg"
outputFile="output.jpg"

 #创建画布
im=Image.open(inputSrc+inputFile)

draw = ImageDraw.Draw(im)

#由图片大小确定字体大小
fontsize=50

#增加字体
fontobj=ImageFont.truetype(font=fontSrc, size=fontsize, index=0, encoding="")
draw.text((im.size[0]-fontsize,0),text="9", fill=(255,0,0), font=fontobj)

im.save(outputSrc+outputFile)

im.show()
