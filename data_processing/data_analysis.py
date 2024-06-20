"""
 coding=utf-8
 @Software: PyCharm
 @Date: 2024/3/23 22:46
 @Author: Glimmering
 @Function: 对爬取的数据进行分析
"""

import random
import time
import csv
import json
import re

import jieba
import jieba.analyse
import numpy as np
import pandas as pd
import sklearn
import codecs
import chardet
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from lxml import etree
import requests
import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 模拟键盘操作
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains
import os
import json
from PIL import Image
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import socket
from itertools import chain
from pypinyin import pinyin, Style  # 对中文按照拼音排序
from multiprocessing import Pool  # 导入进程池
from bs4 import BeautifulSoup

socket.setdefaulttimeout(30)  # 设置socket层的超时时间为20秒


# C - 2 清洗数据
class DataAnalysis:
    __doc__ = "数据分析"

    def __init__(self):
        pass

    # 1 - 分析每位作者的作品数量
    def author_work_cnt(self):
        author_rank = []
        root = '../completion_authors_works/txt/'
        for folder_path, folder_name, file_names in os.walk(root):
            for file in file_names:
                author = file.split('.')[0]
                path = root + author + '.txt'
                with open(path, 'r', encoding='utf-8') as f:
                    work_cnt = len(f.readlines())  # 计算作品个数
                    author_rank.append({author: work_cnt})
                    f.close()
            break

        # tmp_rank = list(.items())  # 得到列表: L=[('a', 1), ('c', 3), ('b', 2)]

        # L.sort(key=lambda x: x[1], reverse=False)  # 按列表中，每一个元组的第二个元素从小到大排序。
        author_rank = sorted(author_rank, key=lambda x: x[0], reverse=True)
        print(author_rank)

        path = '../completion_authors_works/author_rank.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(author_rank, f, indent=4, ensure_ascii=False)
            f.close()

        path = '../completion_authors_works/author_rank.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for author in author_rank:
                json.dump(author, f, ensure_ascii=False)
                f.write('\n')
            f.close()


# 1 - 测试
def test():
    da = DataAnalysis()
    da.author_work_cnt()


if __name__ == '__main__':
    test()
