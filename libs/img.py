# -*- coding:utf-8 -*-  

"""
* 0010
    使用 Python 生成类似于下图中的字母验证码图片
    2017/1/28
"""

import random
from PIL import Image, ImageDraw, ImageFont

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

root = ""
a = ord('a')
A = ord('A')
for i in range(0, 26):
    root += chr(a + i)
    root += chr(A + i)

# bgImg = Image.open("background.png")
# bgImg.show()

font = ImageFont.truetype(r'./Jokerman_Regular.woff.ttf', 60) # 创建字体对象给ImageDraw中的text函数使用

for j in range(0, 10):
    ans = ""
    for i in range(0, 4):
        ans += random.choice(root)
    # print(ans)

    bg_color = randomColor()
    bgImg = Image.new('RGB', (185, 90), bg_color) # 新建一个图片对象, 背景颜色随机
    # bgImg.show()
    canvas = ImageDraw.Draw(bgImg)

    text_color = randomColor()
    while(colorDifference(bg_color, text_color) < 100): # 让字体颜色和背景颜色反差大一些，以防看不清
        text_color = randomColor()

    canvas.text((0, 0),ans, text_color, font)

    name =   ans + '.gif'
    bgImg.save(name, 'gif')
    rstImg = Image.open(name)
    rstImg.show()

    inp = input('Please type in the characters in the image:')
    while inp != ans:
        inp = input('Incorrect input. Please try again:')
