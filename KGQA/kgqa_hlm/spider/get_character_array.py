# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/3/5 13:14
 @Author: Glimmering
 @Function: 获取人物信息
"""

import codecs


def get_character():
    f = codecs.open('./json/hlm_relation.txt', 'r', 'utf-8')
    data = []
    for line in f.readlines():
        array = line.strip("\n").split(",")
        arr = [array[0], array[1]]
        data.extend(arr)

    return data
