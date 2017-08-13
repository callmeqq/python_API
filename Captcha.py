#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytesseract
from PIL import Image
import StringIO


# 获取出现次数最多的灰度，认为出现次数最多的灰度为 有效灰度
def __get_rgb_count(img):
    rgb_list = []
    rgb_count = {}
    for y in range(22):
        rgb = img.getpixel((7, y))
        rgb_list.append(rgb)
        if rgb < 249:
            # 记录灰度的位置和出现次数
            rgb_count[y] = rgb_list.count(rgb)
    # 给dict按出现次数排序，得到出现次数最多的灰度值所在的位置
    sort_rgb_count = sorted(rgb_count.items(), key=lambda d: d[1], reverse=True)
    return rgb_list[sort_rgb_count[0][0]]


# 生成一张映射表，当灰度为 有效灰度 时为黑色，其他为白色
def __init_table(threshold):
    table = []
    for i in range(256):
        if i == threshold:
            table.append(0)
        else:
            table.append(1)
    return table


# 返回切割后并处理好的子图片
def __get_child_image(img):
    child_image_list = []
    for i in range(4):
        # 切割图片的起始坐标
        x = 4 + i * (15 + 15)
        y = 5
        # 切割图片，长22，宽15
        child_image = img.crop((x, y, x + 15, y + 22))
        # 获取出现次数最多的灰度,即 有效灰度
        threshold = __get_rgb_count(child_image)

        # 利用point对图片映射，使图片二值化，去除了干扰线和噪点
        child_image_after = child_image.point(__init_table(threshold), '1')

        child_image_list.append(child_image_after)
    return child_image_list


def get_captcha(captcha_response):
    captcha_list = []
    # captcha_response = requests.get('http://jwxt.ecjtu.jx.cn/servlet/code.servlet')
    # 通过stringIO将验证码图片放入内存，省去保存到本地再读取
    image_buff = StringIO.StringIO(captcha_response.content)
    captcha_image = Image.open(image_buff)
    # 释放内存
    image_buff.close()
    # captcha_image.show()
    # 将图片转换为灰度图像
    im = captcha_image.convert('L')
    image_list = __get_child_image(im)
    for x in image_list:
        captcha_code = pytesseract.image_to_string(x, config='-psm 8')
        # 每次都把'9'识别成'.' 将识别出的'.'替换成9
        if captcha_code == '.':
            captcha_code = '9'
        captcha_list.append(captcha_code)
    # 将list转换为string
    code = "".join(captcha_list)
    # print code
    return code
