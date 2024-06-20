# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/10 13:34
 @Author: Glimmering
 @Function: 展示人物的相关数据
"""

import codecs
import json
import os

# 获取当前路径
path = '/'.join(os.path.abspath(__file__).split('\\')[:-1]) + '/json/data.json'
with open(path, encoding='utf-8') as f:
    data = json.load(f)


def get_profile(name):
    s = ''
    for i in data[name]:
        st = "<dt class = \"basicInfo-item name\" >" + str(i) + " \
        <dd class = \"basicInfo-item value\" >" + str(data[name][i]) + "</dd >"
        s += st
    return s
