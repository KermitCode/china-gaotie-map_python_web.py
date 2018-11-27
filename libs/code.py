#!/usr/bin/python
#coding=utf8

import random
from PIL import Image, ImageDraw, ImageFont
import io
import StringIO

def randomColor():
    r = random.randint(0, 256)
    g = random.randint(0, 256)
    b = random.randint(0, 256)
    return (r, g, b)

def colorDifference(bg_color, text_color):
    d = 0
    for i in range(0, 3):
        d += (text_color[i] - bg_color[i]) ^ 2
    return d

def getcode():
    ans = ""
    for i in range(0, 4):
        ans += random.choice('0123456789')
    return ans

def makeimg(codechar):
    bg_color = randomColor()
    bgImg = Image.new('RGB', (70, 30), bg_color) # 新建一个图片对象, 背景颜色随机
    # bgImg.show()
    canvas = ImageDraw.Draw(bgImg)
    
    font = ImageFont.truetype(r'libs/Jokerman_Regular.woff.ttf', 20) # 创建字体对象给ImageDraw中的text函数使用
    #font = ImageFont.truetype(r'./Jokerman_Regular.woff.ttf', 60) # 创建字体对象给ImageDraw中的text函数使用
    text_color = randomColor()
    while(colorDifference(bg_color, text_color) < 100): # 让字体颜色和背景颜色反差大一些，以防看不清
        text_color = randomColor()

    canvas.text((8, 0), codechar, text_color, font)

    buf = StringIO.StringIO()
    bgImg.save(buf, "gif")
    contents = buf.getvalue()
    buf.close()
    return contents


    #path = 'cache/' + codechar + '.gif'
    #out = io.BytesIO()
    #bgImg.save(out, 'gif')
    #content = out.getvalue()
    ##out.close()
    #return content 
