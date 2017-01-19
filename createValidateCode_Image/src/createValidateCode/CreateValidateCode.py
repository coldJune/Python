#coding:utf-8
'''
Created on 2017年1月18日

@author: coldJune
'''
from PIL import Image
import random,string
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
fontpath="./../../font/STXINGKA.TTF"
savepath="./../../image/"
#获得随机生成的四个字母
def createCode():
    codes=[random.choice(string.ascii_letters) for _ in range(4)]
    return codes

#获得颜色
def createColor():
    colors=(random.randint(30,100),random.randint(30,100),random.randint(30,100))
    return colors

#创建验证码图片
def createPicture():
    width=240
    height=60
    #创建画布
    image=Image.new('RGB',(width,height),(180,180,180))
    fon=ImageFont.truetype(fontpath,40)
    draw=ImageDraw.Draw(image)
    
    #创建验证码对象
    code=createCode()
    
    #把验证码画在画布上
    for i in range(4):
            draw.text((60*i+10,0),code[i],font=fon,fill=createColor())
            
            
    #添加噪点
    for i in range(random.randint(1500,3000)):
        draw.point((random.randint(0,width),random.randint(0,height)),fill=createColor())
        
    #模糊处理
    image.show()
    image=image.filter(ImageFilter.BLUR)
    
    #保存名字为验证码的图片
    image.save(savepath+'code.jpg','jpeg')
    
if __name__=='__main__':
    createPicture()