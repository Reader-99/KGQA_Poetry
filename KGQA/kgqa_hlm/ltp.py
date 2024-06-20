# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/10 13:34
 @Author: Glimmering
 @Function: 使用ltp的模型，完成ner、cws等任务
"""

import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer

ltp_path = '../models/ltp_model/'  # ltp模型目录的路径


def cut_words(words):
    """
    分词
    :param words: 待分句子
    :return: 分词列表
    """
    # 词性标注模型路径，模型名称为`pos.model`
    # cws_model_path = os.path.join(ltp_path, "cws.model")
    # postagger = Postagger()  # 初始化实例
    # postagger.load(pos_model_path)  # 加载模型
    try:
        segmentor = Segmentor(ltp_path + "cws.model")  # 加载 分词 模型

        # segmentor = pyltp.Segmentor()
        # seg_model_path = os.path.join(ltp_path, 'cws.model')

        # segmentor.load(seg_model_path)

        words = segmentor.segment(words)
        array_str = "|".join(words)
        array = array_str.split("|")
        segmentor.release()
        return array

    except Exception as e:
        print(e)


# 林黛玉的父亲是谁？
def words_mark(array):
    # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger(ltp_path + "pos.model")
    postags = postagger.postag(array)  # 词性标注

    pos_str = ' '.join(postags)
    pos_array = pos_str.split(" ")
    postagger.release()  # 释放模型
    print(pos_array)   #获取 词性标注
    return pos_array


def get_target_array(words):   # 命名实体识别
    target_pos = ['nh', 'n']
    target_array = []
    seg_array = cut_words(words)
    pos_array = words_mark(seg_array)

    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])

    target_array.append(seg_array[1])

    if target_array:  # 正确话语
        return target_array
    else:
        return None
