"""
 coding=utf-8
 @Software: PyCharm
 @Date: 2024/3/22 10:56
 @Author: Glimmering
 @Function: 操作各类数据集，获取需要的知识，进行知识融合和补全
"""

import opencc


class KnowledgeCompletion:
    __doc__ = "知识补全"

    # 1 - 繁体转换为简体
    def traditional_to_simplify(self, text):
        cc = opencc.OpenCC('t2s')
        return cc.convert(text)

    # 2 -


# 1 - 处理数据
def process_data():
    kc = KnowledgeCompletion()

    text = "帝姓李氏，諱世民，神堯次子，聰明英武。貞觀之治，庶幾成康，功德兼隆。由漢以來，未之有也。而銳情經術，初建秦邸，即開文學館，召名儒十八人爲學士。既即位，殿左置弘文館，悉引內學士，番宿更休。聽朝之間，則與討論典籍，雜以文詠。或日昃夜艾，未嘗少怠。詩筆草隸，卓越前古。至於天文秀發，沈麗高朗，有唐三百年風雅之盛，帝實有以啓之焉。在位二十四年，諡曰文。集四十卷。館閣書目，詩一卷，六十九首。今編詩一卷。"
    print(kc.traditional_to_simplify(text))


if __name__ == '__main__':
    process_data()