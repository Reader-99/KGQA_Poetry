# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/3/19 21:43
 @Author: Glimmering
 @Function: 手写爬虫脚本，多进程爬取
"""

import random
import sys
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
import opencc  # 繁体和简体转换
from logger import Logger
import shutil  # 文件复制
import tqdm  # 任务完成进度条

socket.setdefaulttimeout(30)  # 设置socket层的超时时间为20秒


# C - 1 爬取数据
class Spider:
    def __init__(self):
        self.domain = "http://so.gushiwen.cn"
        self.headers = {'user-agent': UserAgent().random}
        self.type_name = ''  # 使用进程爬虫时，得到相应的名字
        self.work_types = []

    # 1、解析网页
    def parser_url(self, url):
        response = requests.get(url, headers=self.headers)
        html_text = response.content.decode()
        html = etree.HTML(html_text, etree.HTMLParser())
        response.close()  # 注意关闭response
        time.sleep(1)  # 自定义
        return html  # 返回解析树

    # 2、更新网站数据 - 各朝代和各个作者对应的链接
    def update_data(self):
        """
        start_url = "https://so.gushiwen.cn/authors"  # 爬取的起始链接
        response = requests.get(start_url, headers=self.headers)
        html_text = response.content.decode()
         # 获取朝代链接
        path = '../txts/authors_html.txt'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_text)
            f.close()
        """

        path = '../txts/authors_html.txt'
        with open(path, 'r', encoding='utf-8') as f:
            html_text = f.read()
            f.close()

        html = etree.HTML(html_text, etree.HTMLParser())
        dynasty_urls = html.xpath('//div[@class="sright"]/a')

        path = '../jsons/dynasty_authors.json'  # 解析网页获取各朝代的链接
        dynasty_links = {}
        with open(path, 'w', encoding='utf-8') as f:
            for url in dynasty_urls:  # 遍历各个朝代的作者
                title = url.xpath('./text()')[0]  # xpath 对象 - list
                link = url.xpath('./@href')[0]
                print(title, ' ', link)
                dynasty_links[title] = self.domain + link  # 标题加链接

            json.dump(dynasty_links, f)  # 按 json 格式写入文件
            f.close()

        # 获取各个朝代 作者 的链接
        with open(path, 'r', encoding='utf-8') as f:
            dynasty_links = json.load(f)
            f.close()

        path = '../jsons/authors_name.json'
        author_links = {}
        with open(path, 'w', encoding='utf-8') as f:
            for key, url in dynasty_links.items():
                # print(key, url)
                html = self.parser_url(url)
                author_urls = html.xpath('//div[@class="typecont"]//span/a')
                # print(author_urls)
                for href in author_urls:  # 遍历各个的作者
                    title = href.xpath('./text()')[0]  # xpath 对象 - list
                    link = href.xpath('./@href')[0]
                    print(title, ':', link)
                    author_links[title] = self.domain + link  # 标题加链接

            json.dump(author_links, f)  # 按 json 格式写入文件
            f.close()

        path = '../txts/authors_name.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for key, value in author_links.items():
                f.write(key + ': ' + value + '\n')
            f.close()

    # 3、更新网站数据 - 所有诗文和名句的链接
    def update_author_works(self):
        path = '../jsons/authors_name.json'  # 读取文件
        with open(path, 'r', encoding='utf-8') as f:
            author_links = json.load(f)  # 字典
            f.close()

        authors_works = dict.fromkeys(author_links.keys(), None)  # 字典的键为 作者名字
        authors_famous_sentences = dict.fromkeys(author_links.keys(), None)
        for author, url in author_links.items():  # 处理作者
            try:
                print(author, ": ", url)
                html = self.parser_url(url)  # 解析网页
                if html is None:  # 访问失败
                    print(author + ': ' + url + '--------注意：链接失效，访问失败! 请更新数据！！！-----\n')
                    continue

                # 解析诗文和名句，得到作者的诗文和名句的链接
                div_urls = html.xpath('//div[@class="main3"]/div[@class="left"]'
                                      '/div[@class="sonspic"]/div[@class="cont"]/p/a/@href')  # 根据div分组

                if not div_urls:  # 没有诗文和名句
                    print(author, ": ", url, '注意：没有诗文和名句...')
                    continue

                elif len(div_urls) == 2:  # 既有诗文又有名句
                    authors_works[author] = self.domain + div_urls[0]
                    authors_famous_sentences[author] = self.domain + div_urls[1]

                else:  # 只有诗文或者名句
                    div_tmp = html.xpath(
                        '//div[@class="main3"]/div[@class="left"]'
                        '/div[@class="sonspic"]/div[@class="cont"]/p/a//text()')  # 根据div分组
                    if div_tmp[0][-2:] == '诗文':
                        authors_works[author] = self.domain + div_urls[0]
                    if div_tmp[0][-2:] == '名句':
                        authors_famous_sentences[author] = self.domain + div_urls[0]
                    print(div_tmp[0][-2:])

            except Exception as e:
                # 写入数据 - .json
                path1 = '../jsons/authors_works.json'
                path2 = '../jsons/authors_famous_sentences.json'
                with open(path1, 'w', encoding='utf-8') as f:
                    json.dump(authors_works, f)
                    f.close()
                with open(path2, 'w', encoding='utf-8') as f:
                    json.dump(authors_famous_sentences, f)
                    f.close()

                # 写入数据 - .txt 便于查看
                path1 = '../txts/authors_works.txt'
                path2 = '../txts/authors_famous_sentences.txt'
                with open(path1, 'w', encoding='utf-8') as f:
                    for key, value in authors_works.items():
                        if value is None:
                            f.write(key + ': null' + '\n')
                        else:
                            f.write(key + ': ' + value + '\n')
                    f.close()
                with open(path2, 'w', encoding='utf-8') as f:
                    for key, value in authors_famous_sentences.items():
                        if value is None:
                            f.write(key + ': null' + '\n')
                        else:
                            f.write(key + ': ' + value + '\n')
                    f.close()

                print('\n————————出现异常————————\n')
                print(e)
                continue

        # 写入数据 - .json
        path1 = '../jsons/authors_works.json'
        path2 = '../jsons/authors_famous_sentences.json'
        with open(path1, 'w', encoding='utf-8') as f:
            json.dump(authors_works, f)
            f.close()
        with open(path2, 'w', encoding='utf-8') as f:
            json.dump(authors_famous_sentences, f)
            f.close()

        # 写入数据 - .txt 便于查看
        path1 = '../txts/authors_works.txt'
        path2 = '../txts/authors_famous_sentences.txt'
        with open(path1, 'w', encoding='utf-8') as f:
            for key, value in authors_works.items():
                if value is None:
                    f.write(key + ': null' + '\n')
                else:
                    f.write(key + ': ' + value + '\n')
            f.close()
        with open(path2, 'w', encoding='utf-8') as f:
            for key, value in authors_famous_sentences.items():
                if value is None:
                    f.write(key + ': null' + '\n')
                else:
                    f.write(key + ': ' + value + '\n')
            f.close()

    # 5、更新（处理）网站数据 - 作者的所有信息
    def process_author_message(self, author, url):
        html = self.parser_url(url)  # 解析网页
        if html is None:  # 访问失败
            print(author + ': ' + url + '--------注意：链接失效，访问失败! 请更新数据！！！-----\n')
            return

        #  F - 1获取作者所有介绍
        div_data = html.xpath(
            '//div[@class="main3"]/div[@class="left"]')[0]  # 根据div分组
        print('div——list', div_data)

        # 1、获取简介
        """
        tmp = div_data.xpath('div[@class="sonspic"]/div[@class="cont"]/p//text()')[0]
        author_bi = tmp if tmp else None

        # 2、获取每个小标题
        title = div_data.xpath('//div[@class="contyishang"]//h2//text()')
        print(title)
        items = dict.fromkeys(title, None)

        # 3、获取每个标题的内容
        tmp = div_data.xpath('//div[@class="contyishang"]')
        for i in range(len(tmp)):
            text = tmp[i].xpath('./p//text()')
            if not text:  # 存在超链接
                # print(text)
                text = tmp[i].xpath('.//text()')[-1]  # 取出最后的文本
                text = text.strip('\r\n')
                text = text.replace('\u3000\u3000', "")
                text = text.replace(" ", "")
                items[title[i]] = text  # 标题加文本
                # print(title[i] + ': ' + text)
                continue

            tmp_1 = ''
            for j in text:
                j = j.strip('\r\n')
                j = j.replace('\u3000', "")
                j = j.replace(" ", "")
                tmp_1 += j[2:]  # 去除不同编码之间不容而导致的空格
            items[title[i]] = tmp_1[:len(tmp_1) - 20]
            # print(title[i] + ': ' + tmp_1[:len(tmp_1) - 20])

        # 5、将所有内容写入文件
        root = self.root + '/作者/' + author + '的简介'  # 创建根目录
        if not os.path.exists(root):  # 创建根目录
            os.mkdir(root)

        path = root + '/' + author + '的简介.txt'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(author + ': ' + url + '\n')
            f.write('人物简介' + ': ' + author_bi + '\n')
            for title, content in items.items():
                f.write(title + ': ' + content + '\n')
            f.close()
        """
        # 6、获取图片
        root = self.root + '/作者/' + author + '的简介'  # 创建根目录

        try:
            image = div_data.xpath('div[@class="sonspic"]/div[@class="cont"]/div[@class="divimg"]/img/@src')
            # image = str(image)
            # print('image', image)
            path = root + '/{}.jpg'.format(author)
            r = requests.get(image[0], self.headers)  # 伪装浏览器访问
            # print(r.content) # 全为二进制文件
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
        except Exception as e:
            print('抱歉，链接访问失败！')
            print(e)
            return

    # 6、更新网站 作品以及名句 的类型
    def update_work_sen_types(self):
        # 1 - 更新 诗文 的类型
        start_url = "https://so.gushiwen.cn/shiwens/"
        html = self.parser_url(start_url)  # 解析网页
        if html is None:  # 访问失败
            print('--------注意：链接失效，访问失败! 请更新数据！！！-----\n')

        # 解析诗文和名句，得到作者的诗文和名句的链接
        type_urls = html.xpath('//div[@class="main3"]//div[@class="titletype"]'
                               '//div[@class="sright"]/a/@href')  # 根据div分组
        type_name_urls = html.xpath('//div[@class="main3"]//div[@class="titletype"]'
                                    '//div[@class="sright"]/a/text()')  # 根据div分组
        works_types = {}
        for i in range(len(type_urls)):
            print(type_name_urls[i] + " " + type_urls[i])
            works_types[type_name_urls[i]] = self.domain + type_urls[i]
            if i == 77:  # 只要前面的类型，去除其他分类
                break

        path = '../jsons/works_types.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(works_types, f)
            f.close()

        path = '../txts/works_types.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for work_type, url in works_types.items():
                f.write(work_type + ' ' + url)
                f.write('\n')
            f.close()

        # 2 - 更新 名句 的类型
        start_url = "https://so.gushiwen.cn/mingjus/"
        html = self.parser_url(start_url)  # 解析网页
        if html is None:  # 访问失败
            print('--------注意：链接失效，访问失败! 请更新数据！！！-----\n')

        # 解析诗文和名句，得到作者的诗文和名句的链接
        type_urls = html.xpath('//div[@class="main3"]//div[@class="titletype"]'
                               '//div[@class="sright"]/a/@href')  # 根据div分组
        type_name_urls = html.xpath('//div[@class="main3"]//div[@class="titletype"]'
                                    '//div[@class="sright"]/a/text()')  # 根据div分组
        works_types = {}
        for i in range(len(type_urls)):
            works_types[type_name_urls[i]] = self.domain + type_urls[i]
            if i == 83:
                break

        path = '../jsons/sentences_types.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(works_types, f)
            f.close()

        path = '../txts/sentences_types.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for work_type, url in works_types.items():
                f.write(work_type + ' ' + url)
                f.write('\n')
            f.close()

    # 7、爬取所有类型对应的作品
    def works_type_pages(self, type_page):
        html = self.parser_url(type_page)  # 解析网页
        if html is None:  # 访问失败
            print('注意: 此页没有数据！！！' + type_page)
            return

        # 解析该类型包含的作品（title, author, dynasty, type）
        works = html.xpath('//div[@class="main3"]//div[@id="leftZhankai"]//div[@class="cont"]')  # 根据div分组
        if works is None:
            return

        titles = works[0].xpath('//p/a/b/text()')
        tmp_authors = works[0].xpath('//p/a/text()')

        if titles is None:
            return

        authors = []
        for author in tmp_authors:  # 清洗作者和朝代
            if author == '\n':
                continue
            if '\n' in author:
                author = author.replace('\n', '')
            elif '〔' in author:
                author = author.replace('〔', '').replace('〕', '')

            authors.append(author)

        print(titles)
        print(authors)
        i = 0  # 名字和朝代
        for idx, title in enumerate(titles):
            works_type = {
                "title": title,
                "author": authors[i],
                "dynasty": authors[i + 1],
                "type": self.type_name,
            }  # 作品的类型
            self.work_types.append(works_type)
            i = i + 2

    # 8、获取所有朝代的诗人，用于知识补全
    def author_and_dynasty(self, url):
        try:
            time.sleep(1)
            headers = {'user-agent': UserAgent().random}
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            html = r.text

            soup = BeautifulSoup(html, features='lxml')
            urls = soup.select('a[href]')  # 找到本网页所有的 a 标签

            # 只取得包含名字和朝代 url
            tmp_urls = []
            for i in range(len(urls))[53:]:  # 53之前全相同
                if '首页' in str(urls[i]):
                    break
                if 'img' in str(urls[i]) or '的诗文' in str(urls[i]):
                    continue
                tmp_urls.append(urls[i])

            # 获得 名字和朝代
            dynasty_of_authors = []

            i = 0
            url_len = len(tmp_urls)
            while i < url_len:
                dynasty_and_author = {}
                name = tmp_urls[i].get_text()  # 获取名字
                dynasty = tmp_urls[i + 1].get_text()  # 获取名字
                print(name + " " + dynasty)
                dynasty_and_author[name] = dynasty
                dynasty_of_authors.append(dynasty_and_author)
                i += 2

            path = '../txts/authors_details/authors_of_dynasty.txt'
            with open(path, 'a', encoding='utf-8') as f:
                for author in dynasty_of_authors:
                    json.dump(author, f, ensure_ascii=False)
                    f.write('\n')
                f.close()

        except Exception as e:
            print("发生异常：url: ", url)
            return

    # 9、处理网站数据  - 作者的所有诗文
    def process_author_poems(self, author, url):
        html = self.parser_url(url)  # 保证初始网页能够访问
        if html is None:  # 访问失败
            print(author + ': ' + url + '--------注意：链接失效，访问失败! 请更新数据！！！-----\n')
            return

        next_url = url
        header = ['url', '题目', '作者', '朝代', '原文']
        poems_data = []

        while next_url is not None:
            html = self.parser_url(next_url)  # 解析多页网页
            if html is None:  # 访问失败
                print(author + ': ' + url + '--------注意：链接失效，访问失败! 请更新数据！！！-----\n')
                return

            all_data = html.xpath('//div[@id="leftZhankai"]//div[@class="sons"]')  # 根据div分组
            # print(all_data)
            for div_data in all_data:  # 遍历所有所有需要的内容
                poem_data = []
                # 1、 获取题目和url
                tmp = div_data.xpath('./div[@class="cont"]/p/a/@href')
                title_url = self.domain + tmp[0] if tmp else None
                poem_data.append(title_url)
                # print(title_url)

                tmp = div_data.xpath('./div[@class="cont"]/p/a/b/text()')
                title = tmp[0] if tmp else None
                poem_data.append(title)
                # print(title)

                # 3、获取朝代
                poem_data.append(author)  # 将作者加入
                tmp = div_data.xpath('./div[@class="cont"]/p[@class="source"]/a/text()')
                dynasty = tmp[1] if tmp else None
                poem_data.append(dynasty)
                # print(dynasty)

                # 3、原文
                tmp = div_data.xpath('./div[@class="cont"]/div[@class="contson"]//text()')
                # print(tmp)
                tmp_text = tmp if tmp else None
                source_text = ''
                try:
                    for text in tmp_text:  # 获取原文的列表
                        text = text.replace('\r\n                    ', '')
                        text = text.replace('\r\n', '')
                        text = text.replace('\r\n                ', '')
                        text = text.replace('\u3000', '')
                        source_text += text + '\n'
                except Exception as e:
                    print(e)
                    continue

                poem_data.append(source_text)
                # print(source_text)
                poems_data.append(poem_data)  # 将各个诗词放入列表

            # 进入下一页
            tmp = html.xpath('//div[@class="pagesright"]/a[@class="amore"]/@href')
            next_url = self.domain + tmp[0] if tmp else None
            # print('next_url:', next_url)

        # 5、将所有内容写入文件
        path = self.root + '/诗文/' + author + '的诗文.csv'  # 创建根目录
        with open(path, 'w', encoding='utf-8-sig', newline="") as f:
            writer = csv.writer(f)  # 基于打开的文件，创建 csv.writer 实例
            writer.writerow(header)  # 写入 header 一次只能写入一行。
            writer.writerows(poems_data)  # 写入数据 一次写入多行
            f.close()
        # print(poems_data)


# C - 2 清洗数据
class Clean_Data:
    def __init__(self):
        self.spider = Spider()

    # 1 - 清洗作者没有相关诗文和名句的
    def process_authors_works(self):
        # 清洗作品
        path = '../jsons/authors_works.json'
        with open(path, 'r', encoding='utf-8') as f:
            authors_works = json.load(f)
            f.close()

        tmp_works = {}
        for name, work in authors_works.items():
            if work:
                tmp_works[name] = work

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(tmp_works, f)  # 按 json 格式写入文件
            f.close()

        # 清洗名句
        path = '../jsons/authors_famous_sentences.json'
        with open(path, 'r', encoding='utf-8') as f:
            authors_famous_sentences = json.load(f)
            f.close()

        tmp_sentence = {}
        for name, sentence in authors_famous_sentences.items():
            if sentence:
                tmp_sentence[name] = sentence

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(tmp_sentence, f)  # 按 json 格式写入文件
            f.close()

    # 2 - 将 json 转为 txt 文件
    def json_to_txt(self):
        path = '../jsons/authors_works.json'
        with open(path, 'r', encoding='utf-8') as f:
            authors_works = json.load(f)
            f.close()

        path = '../jsons/authors_famous_sentences.json'
        with open(path, 'r', encoding='utf-8') as f:
            authors_famous_sentences = json.load(f)
            f.close()

        # 写入数据 - .txt 便于查看
        path1 = '../txts/authors_works.txt'
        path2 = '../txts/authors_famous_sentences.txt'
        with open(path1, 'w', encoding='utf-8') as f:
            for key, value in authors_works.items():
                f.write(key + ': ' + value + '\n')
            f.close()

        with open(path2, 'w', encoding='utf-8') as f:
            for key, value in authors_famous_sentences.items():
                f.write(key + ': ' + value + '\n')
            f.close()

    # 3 - 将作者与朝代对应
    def dynasty_of_author(self):
        path = '../jsons/dynasty_authors.json'  # 获取每个朝代的链接
        with open(path, 'r', encoding='utf-8') as f:
            dynastys = json.load(f)
            f.close()

        path = '../jsons/authors_name.json'  # 获取所有作者
        with open(path, 'r', encoding='utf-8') as f:
            author_name = json.load(f)
            f.close()

        dynasty_of_author = dict.fromkeys(author_name.keys(), None)
        for dynasty, url in dynastys.items():
            try:
                html = self.spider.parser_url(url)
                if html is None:  # 访问失败
                    print(dynasty + ':' + url + '--------注意：链接失效，访问失败! 请更新数据！！！-----\n')
                    continue

                # 将作者与朝代对应
                author_urls = html.xpath('//div[@class="typecont"]//span/a')
                for href in author_urls:  # 遍历各个的作者
                    author_name = href.xpath('./text()')[0]  # xpath 对象 - list
                    print(author_name, ":", dynasty)
                    dynasty_of_author[author_name] = dynasty

            except Exception as e:
                # 写入数据 - .json
                path = '../jsons/authors_details/dynasty_of_author.json'
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(dynasty_of_author, f)
                    f.close()

                path = '../txts/authors_details/author_of_dynasty.txt'
                with open(path, 'w', encoding='utf-8') as f:
                    for key, value in dynasty_of_author.items():
                        f.write(key + ':' + value + '\n')
                    f.close()
                print('\n————————出现异常————————\n')
                print(e)
                continue

        # 写入数据 - .json
        path = '../jsons/authors_details/dynasty_of_author.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(dynasty_of_author, f)
            f.close()

        path = '../txts/authors_details/author_of_dynasty.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for key, value in dynasty_of_author.items():
                f.write(key + ':' + value + '\n')
            f.close()

    # 4 - 构建实体 作品（静夜思）的属性
    def create_properties(self):
        root = "D:/5.2_py_fs/cd_1/诗文/"

        works = []
        for folder_path, folder_name, file_names in os.walk(root):
            works = [root + i for i in file_names]
            break

        for work in works:  # 处理所有作者的作品
            print(work)
            author_works = []
            author_works_urls = {}

            df = pd.read_csv(work)
            urls = df['url']
            if len(urls) == 0:
                continue

            titles = df['题目']
            author = df['作者'][0]  # 作者和朝代都一样

            dynasty = df['朝代'][0]
            dynasty = dynasty.split('〕')[0][1:]  # 获取朝代

            contents = df['原文']

            url_len = len(urls)
            for i in range(url_len):
                url = urls[i]
                title = titles[i]

                content = contents[i]  # 格式化字符串
                result = ''
                tmp = content.replace('\n', '').replace(' ', '')
                for k in range(len(tmp)):
                    if tmp[k] in " \n # & \t ":
                        continue
                    elif tmp[k] in "。？！":
                        result += tmp[k] + '\n'
                    else:
                        result += tmp[k]

                content = result
                author_work = {
                    "title": title,
                    "author": author,  # 作者都一样
                    "dynasty": dynasty,
                    "content": content,
                    "translation": None,
                    "annotation": None,
                    "background": None,
                    "appreciation": None
                }  # 每个作者的作品集
                author_works.append(author_work)
                author_works_urls[title] = url  # 键值对 ： title:url

            # json格式 写入文件
            path = '../txts/authors_works/' + author + '.txt'
            with open(path, 'w', encoding='utf-8') as f:
                for author_work in author_works:
                    json.dump(author_work, f)
                    f.write('\n')
                f.close()

            # 写入 题目与url
            path = '../jsons/authors_works_urls/' + author + '.json'
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(author_works_urls, f)
                f.close()

            path = '../txts/authors_works_urls/' + author + '.txt'
            with open(path, 'w', encoding='utf-8') as f:
                for title, url in author_works_urls.items():
                    f.write(title + ':' + url)
                    f.write('\n')
                f.close()

    # 5 - 将 txt 转 json - 作品类型、名句类型
    def txt_to_json(self):
        # root = '../txts/sentences_types/'   # 转换 名句-类型 保存
        # target_root = '../jsons/sentences_types/'

        # root = '../txts/works_types/'  # 转换 作品-类型 保存
        # target_root = '../jsons/works_types/'

        root = '../txts/authors_works/'  # 转换 作者-作品 保存
        target_root = '../jsons/authors_works/'

        sentences_types = []
        target_paths = []
        type_filter = ["古文观止", "乐府", "楚辞", "小学古诗", "初中古诗", "高中古诗", "小学文言文"
            , "初中文言文", "高中文言文", "唐诗三百首", "古诗三百首", "宋词三百首"]
        for folder_path, folder_name, file_names in os.walk(root):
            for i in file_names:
                if i in type_filter:
                    sentences_types.append(root + i)
                    target_paths = [target_root + i.split('.')[0] + '.json' for i in file_names]
                    # sentences_types = [root + i for i in file_names]
            break

        file_len = len(sentences_types)
        for i in range(file_len):
            f_json = open(target_paths[i], 'w', encoding='utf-8')
            with open(sentences_types[i], 'r', encoding='utf-8') as f:
                lines = f.readlines()
                all_sentences = []
                for line in lines:  # 每行都是名句
                    sentence_type = json.loads(line)
                    all_sentences.append(sentence_type)

                json.dump(all_sentences, f_json, indent=4, ensure_ascii=False)  # 缩进的空格数，设置为非零值时，就起到了格式化的效果，比较美观

    # 6 - 将所有名句归并，形成名句总文件
    def merge_famous_sentences(self):
        # 获取作者和对应朝代
        path = '../jsons/authors_details/dynasty_of_author.json'
        with open(path, 'r', encoding='utf-8') as f:
            authors_and_dynasty = json.load(f)
            f.close()

        match_sentence = {}
        path = '../jsons/authors_fs/total_sentences.json'
        with open(path, 'r', encoding='utf-8') as f:
            famous_sentences = json.loads(f.read())
            for famous_sentence in famous_sentences:
                content = famous_sentence['content']
                author = famous_sentence['author']
                match_sentence[content] = author
            f.close()

        # 开始匹配
        path = '../jsons/authors_fs/famous_sentence1.json'  # 没有朝代
        merge_sentences = []  # 待写入的名句
        with open(path, 'r', encoding='utf-8') as f:
            famous_sentences = json.loads(f.read())
            for famous_sentence in famous_sentences:
                print(type(famous_sentence))
                print(famous_sentence)
                author = famous_sentence['author']
                content = famous_sentence['content']

                # 特殊情况

                if content not in match_sentence:  # 没有重复
                    print('没有重复的名句为：' + content)
                    print('名字', famous_sentence['author'])

                    if author in authors_and_dynasty:  # 保证知道作者的朝代
                        famous_sentence['dynasty'] = authors_and_dynasty[author]
                    merge_sentences.append(famous_sentence)
                else:
                    if author == match_sentence[content]:  # 已经存在
                        continue
                    else:
                        print('没有重复的名句为：' + content)
                        print("作者为：" + author + '\n')
                        if author in authors_and_dynasty:  # 保证知道作者的朝代
                            famous_sentence['dynasty'] = authors_and_dynasty[author]
                        merge_sentences.append(famous_sentence)
                exit()
            f.close()

        # 保存没有重复的名句
        path = '../jsons/authors_fs/not_repetition_sentences.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(merge_sentences, f, indent=4, ensure_ascii=False)  # 缩进的空格数，设置为非零值时，就起到了格式化的效果，比较美观
            f.close()

        path = '../txts/authors_fs/not_repetition_sentences.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for sentence in merge_sentences:
                json.dump(sentence, f, ensure_ascii=False)
                f.write('\n')
            f.close()

    # 7 - 将所 有朝代有作者 对应
    def dynasties_of_authors(self):
        dynasties_of_authors = {}
        path = '../txts/authors_details/authors_of_dynasty.txt'
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                tmp = dict(json.loads(line))
                for i, j in tmp.items():
                    author = i
                    dynasty = j
                if dynasty not in dynasties_of_authors:
                    dynasties_of_authors[dynasty] = [author]
                else:
                    dynasties_of_authors[dynasty].append(author)

        path = '../jsons/authors_details/authors_of_dynasty.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(dynasties_of_authors, f, indent=2, ensure_ascii=False)

    # 8 - 统一朝代 （清代 - 清朝）
    def unify_dynaty(self):
        path = '../txts/authors_fs/total_sentences.txt'

        all_sentences = []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            dynasties = []
            for line in lines:  # 每行都是名句
                sentence = json.loads(line)

                dynasty = sentence['dynasty']
                if dynasty is None:
                    sentence['dynasty'] = "未知"

                elif dynasty == "隋代":
                    sentence['dynasty'] = "隋朝"

                elif dynasty == "元代":
                    sentence['dynasty'] = "元朝"

                elif dynasty == "清代":
                    sentence['dynasty'] = "清朝"

                elif dynasty == "春秋":
                    sentence['dynasty'] = "先秦"

                elif dynasty == "战国":
                    sentence['dynasty'] = "先秦"

                elif dynasty == "战国初":
                    sentence['dynasty'] = "先秦"

                elif dynasty == "春秋战国":
                    sentence['dynasty'] = "先秦"

                all_sentences.append(sentence)  # 写入文件

                if dynasty not in dynasties:
                    dynasties.append(dynasty)

            f.close()
        for tmp in dynasties:
            print(tmp)

        path = "../txts/authors_fs/total_sentences.txt"
        with open(path, 'w', encoding='utf-8') as f:
            for sentence in all_sentences:
                json.dump(sentence, f, ensure_ascii=False)
                f.write('\n')
            f.close()

        path = "../jsons/authors_fs/total_sentences.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(all_sentences, f, indent=4, ensure_ascii=False)
            f.close()

    # 9 - 填补18000个作者的朝代
    def completion_author_dynasty(self):
        path = '../jsons/authors_details/dynasty_of_author.json'
        with open(path, 'r', encoding='utf-8') as f:
            dynasty_of_author = json.load(f)
            f.close()

        root = '../completion_authors_works/json/'
        for folder_path, folder_name, file_names in os.walk(root):
            target_paths = [root + i for i in file_names]
            # sentences_types = [root + i for i in file_names]
            break

        for path in target_paths:
            print(path)
            with open(path, 'r', encoding='utf-8') as f:
                author_works = json.load(f)
                f.close()

            file = open(path, 'w', encoding='utf-8')
            tmp = []
            for author_work in author_works:
                author = author_work['author']

                if author in dynasty_of_author:  # 填补朝代
                    dynasty = dynasty_of_author[author]
                else:
                    dynasty = "未知"
                author_work['dynasty'] = dynasty

                tmp.append(author_work)

            json.dump(tmp, file, indent=4, ensure_ascii=False)
            file.close()

    # 10 - 获取重复作者的姓名
    def get_repeated_author_name(self):
        path = '../jsons/authors_details/dynasty_of_author.json'
        with open(path, 'r', encoding='utf-8') as f:
            dynasty_of_author = json.load(f)
            f.close()

        # root = '../completion_authors_works/json/'
        root = '../jsons/authors_works/'
        for folder_path, folder_name, file_names in os.walk(root):
            author_names = [i.split('.')[0] for i in file_names]
            # sentences_types = [root + i for i in file_names]
            break

        path = '../jsons/tmp_process/unknow_authors.txt'
        filter_name = ["中庸", "大学", "孟子", "楚辞", "论语", "诗经"]
        file = open(path, 'w', encoding='utf-8')
        for name in author_names:
            if name not in dynasty_of_author and name not in filter_name:
                file.write(name + '\n')
                print("未出现1：" + name)
        file.close()

        root = '../completion_authors_works/json/'
        for folder_path, folder_name, file_names in os.walk(root):
            author_names = [i.split('.')[0] for i in file_names]
            # sentences_types = [root + i for i in file_names]
            break

        path = '../jsons/tmp_process/unknow_authors1.txt'
        filter_name = ["中庸", "大学", "孟子", "楚辞", "论语", "诗经"]
        file = open(path, 'w', encoding='utf-8')
        for name in author_names:
            if name not in dynasty_of_author and name not in filter_name:
                file.write(name + '\n')
                print("未出现2：" + name)

        file.close()

        # path1 = '../jsons/tmp_process/repeated_authors.txt'
        # file1 = open(path1, 'w', encoding='utf-8')
        #
        # path2 = '../jsons/tmp_process/unrepeated_authors.txt'
        # file2 = open(path2, 'w', encoding='utf-8')
        #
        # root = '../jsons/authors_works/'
        # for folder_path, folder_name, file_names in os.walk(root):
        #     for file_name in file_names:
        #         name = file_name.split('.')[0]
        #         if name not in dynasty_of_author:
        #             print("未出现2：" + name)
        #     break

    # 11 - 提取作者节点
    def get_author_nodes(self):
        path = '../jsons/authors_details/dynasty_of_author.json'
        with open(path, 'r', encoding='utf-8') as f:
            dynasty_of_author = json.load(f)
            f.close()

        female_authors = ["庄姜", "许穆夫人", "卓文君", "班婕妤", "班昭", "蔡文姬", "左芬", "苏蕙", "谢道韫",
                          "上官婉儿", "李冶", "薛涛", "刘采春", "鱼玄机", "花蕊夫人", "李清照", "朱淑真", "吴淑姬",
                          "张玉娘", "唐婉", "严蕊", "管道升", "郑允端", "沈宜修", "叶纨纨", "叶小纨", "叶小鸾",
                          "方孟式", "方维仪", "方维则", "李因", "王端淑", "柳如是", "沈善宝", "顾太清", "贺双卿",
                          "吴藻", "陈端生", "蔡琬", "乐昌公主", "张玉孃", "杜秋娘"]  # 不断补充
        all_authors = []
        for author, dynasty in dynasty_of_author.items():
            if author not in female_authors:
                gender = "男"
            else:
                gender = "女"

            tmp = {
                "name": author,
                "gender": gender,
                "dynasty": dynasty,
                "nationality": None,
                "origin": None,  # 出生地
                "date": None,
                "named": None,  # 字、号
                "brief_introduction": None  # 简介
            }
            all_authors.append(tmp)

        path = "../import_nodes/node_author.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(all_authors, f, indent=4, ensure_ascii=False)
            f.close()

        path = "../import_nodes/node_author.txt"
        with open(path, 'w', encoding='utf-8') as f:
            for author in all_authors:
                json.dump(author, f, ensure_ascii=False)
                f.write("\n")
            f.close()

    # 12 - 将未重复的文件进行复制
    def copy_files(self):
        path = '../jsons/tmp_process/unrepeated_authors.txt'
        with open(path, 'r', encoding='utf-8') as f:
            names = f.readlines()
            f.close()

        for name in names:
            name = name.split('\n')[0]
            print(name)
            o_path = '../jsons/authors_works/' + name + '.json'
            t_path = '../completion_authors_works/json/' + name + '.json'
            shutil.copyfile(o_path, t_path)

    # 13 - 对比相同作者的所有作品
    def compare_author_work(self, author):
        path1 = '../completion_authors_works/json/' + author + '.json'
        path2 = '../jsons/authors_works/' + author + '.json'
        with open(path1, 'r', encoding='utf-8') as f:  # 读取所有作品
            works1 = json.load(f)
            f.close()
        with open(path2, 'r', encoding='utf-8') as f:
            works2 = json.load(f)
            f.close()

        all_works = works2

        for work1 in works1:
            title1 = work1['title']
            if '（' in title1 and '）' not in title1:
                title1 = title1 + '）'
                work1['title'] = title1

            if ' ' in title1:
                title1 = title1.replace(' ', '·')

            flag = False
            for work2 in works2:
                title2 = work2['title']
                if '（' in title2 and '）' not in title2:
                    title2 = title2 + '）'
                    work2['title'] = title2

                # 判断标题是否相同
                if title1 == title2 or title1 in title2 or title2 in title1:
                    print(title1 + "---" + title2)
                    tmp_work1 = work1['content'].split('\n')
                    tmp_content = []
                    for i in tmp_work1:
                        tmp_content.extend(i.split('。'))

                    content1 = set(tmp_content)
                    # content1 = set(work1['content'].replace('\n', '').split('。'))

                    # 特殊字符处理
                    tmp_work2 = work2['content'].split('\n')
                    tmp_work21 = []
                    for i in tmp_work2:
                        tmp_work21.append(i.replace('？', '。').replace('！', '。'))

                    content2 = []
                    for i in tmp_work21:
                        content2.extend(i.split('。'))

                    content2 = set(content2)

                    # 判断是否有交集
                    identical_content = content1 & content2
                    print(identical_content)
                    print('len = ', len(identical_content))
                    if len(identical_content) >= 2:  # 有交集，说明是同个作品
                        flag = True

            if not flag:
                tmp_work1 = work1['content'].replace('\n', '').split('。')
                tmp_content = ''
                c_len = len(tmp_work1)
                for i in tmp_work1[:c_len - 1]:
                    tmp_content += i + '。\n'
                work1['content'] = tmp_content
                all_works.append(work1)

        # 写入文件
        path = '../completion_authors_works/identical_author/' + author + '.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(all_works, f, indent=4, ensure_ascii=False)
            f.close()

    # 14 - 将所有作者写入到一个json文件
    def merge_author_works(self):
        # root = '../import_nodes/node_works/node_work1/'
        # root = '../import_nodes/node_works/node_work2/'
        # root = '../import_nodes/node_works/node_work3/'

        root = '../completion_authors_works/json/'
        for folder_path, folder_name, file_names in os.walk(root):
            paths = [root + i for i in file_names]
            # sentences_types = [root + i for i in file_names]
            break

        all_works = []
        for path in paths:
            print(path)
            with open(path, 'r', encoding='utf-8') as f:
                works = json.load(f)
                all_works.extend(works)
                f.close()

        path = '../import_nodes/node_works/node_work.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(all_works, f, indent=4, ensure_ascii=False)
            f.close()

    # 15 - 统计关键信息 - 创建用户字典
    def create_user_dict(self):
        path = '../jsons/authors_fs/total_sentences.json'
        with open(path, 'r', encoding='utf-8') as f:
            sentences = json.load(f)
            f.close()

        all_content = [sentences[0]]
        for sentence in sentences[1:]:
            content = sentence['content']
            flag = False
            for tmp_content in all_content:
                if content != tmp_content['content']:
                    flag = False
                else:
                    flag = True
                    print(sentence)
                    break

            if not flag:
                all_content.append(sentence)

        path = '../txts/user_dict/content.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(all_content, f, indent=4, ensure_ascii=False)
            f.close()

        path = '../txts/user_dict/content.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for sentence in all_content:
                json.dump(sentence, f, ensure_ascii=False)
                f.write('\n')
            f.close()

    # 16 - 统计关键信息 - 得到每位作者的作品
    def get_author_total_works(self):
        path = '../import_nodes/node_work_content.json'
        with open(path, 'r', encoding='utf-8') as f:
            works = json.load(f)
            f.close()

        work_dict = {}
        end_dict = {}

        for work in works:
            author = work['author']
            dynasty = work['dynasty']
            if author not in work_dict:  # 计算作者所有的作品
                work_dict[author] = [1, dynasty]
                end_dict[author] = 1
            else:
                # 需要注意：由于数据来源不同，存在数据错乱的现象。比如同一首诗，题目可能有些许不同
                if dynasty == work_dict[author][1]:  # 相同作者，相同朝代
                    work_dict[author][0] += 1
                    end_dict[author] += 1
                else:
                    print('!!!!!', work)
                    print(work['dynasty'], '!!!!', work_dict[author][1])

        work_dic = sorted(end_dict.items(), key=lambda x: x[1], reverse=True)

        tmp_dict = {}
        path = '../txts/user_dict/author_work_sorted.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for work in work_dic:
                tmp_dict[work[0]] = work[1]
                print(work[0] + " :  " + str(work[1]))
                f.write(work[0] + " :  " + str(work[1]) + '\n')

            f.close()

        path = '../txts/user_dict/author_work_sorted.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(tmp_dict, f, indent=4, ensure_ascii=False)
            f.close()
        # print(dic)

    # 17 - 统计关键信息 - 获取知名作者的作品标题（知名作者：写过10个作品及以上）
    def get_work_title(self):
        path = '../txts/user_dict/author_work_sorted.json'
        with open(path, 'r', encoding='utf-8') as f:
            author_order = json.load(f)
            f.close()

        path = '../import_nodes/node_work_content.json'
        with open(path, 'r', encoding='utf-8') as f:
            works = json.load(f)
            f.close()

        path = '../txts/user_dict/dict_sorted_title.txt'
        f_title = open(path, 'w', encoding='utf-8')
        titles = []
        for work in works:  # 获取知名作者作品的标题
            author = work['author']
            title = work['title']

            if author_order[author] >= 10:  # 根据实际情况做更改
                if title not in titles:
                    titles.append(title)
                    f_title.write(title + '\n')
                else:
                    print(title)

        f_title.close()

    # 18 - 将 json 文件转换为 csv 文件，便于数据的导入
    def change_file(self):
        path = '../data_nodes/node_author.json'
        with open(path, 'r', encoding='utf-8') as f:
            tmp_authors = json.load(f)
            f.close()

        authors = []
        for author in tmp_authors:
            author['nationality'] = 'null'
            author['origin'] = 'null'
            author['date'] = 'null'
            author['named'] = 'null'
            author['brief_introduction'] = 'null'

            authors.append(author)

        path = '../data_csv_nodes/node_author.csv'
        with open(path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['name', 'gender', 'dynasty', 'nationality', 'origin', 'date', 'named', 'brief_introduction']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(authors)


# C - 3 知识补全
class Knowledge_Completion:
    def __init__(self):
        pass

    # 1 - 补全 名句 的属性 - 朝代
    def dynasty_compeltion(self):
        authors = {"左传": "左丘明", "国语": "左丘明", "三国志": "陈寿", "易传": "孔子后学",
                   "抱朴子": "葛洪", "资治通鉴": "司马光", "庄子": "庄子", "鬼谷子": "鬼谷子",
                   "荀子": "荀子", "镜花缘": "李汝珍", "论语": "孔子", "孙子兵法": "孙子",
                   "汉书": "班固", "后汉书": "宋范晔", "春秋": "孔子", "淮南子": "刘安",
                   "墨子": "墨子", "史记": "司马迁", "战国策": "刘向", "菜根谭": "洪应明",
                   "三国演义": "罗贯中", "西游记": "吴承恩", "红楼梦": "曹雪芹", "水浒传": "施耐庵"}
        path = '../jsons/authors_details/dynasty_of_author.json'
        with open(path, 'r', encoding='utf-8') as f:
            dynasty_of_author = json.load(f)
            f.close()

        path = '../jsons/authors_fs/total_sentences.json'
        with open(path, 'r', encoding='utf-8') as f:
            famous_sentences = json.loads(f.read())
            for famous_sentence in famous_sentences:
                author = famous_sentence['author']
                dynasty = famous_sentence['dynasty']

                if author == "":  # 确定名字
                    for title, tmp_author in authors.items():
                        if title in famous_sentence['title']:
                            famous_sentence['author'] = tmp_author
                            famous_sentence['dynasty'] = dynasty_of_author[tmp_author]
                            print('+++++' + title)
                            break

                    if famous_sentence['author'] == "":  # 规整
                        famous_sentence['author'] = None

                if dynasty is None:  # 补全 作者的 朝代
                    print('---' + author + '----')
                    if author in dynasty_of_author:
                        print(dynasty_of_author[author])
                        famous_sentence['dynasty'] = dynasty_of_author[author]
            f.close()

        path = '../jsons/authors_fs/total_sentences.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(famous_sentences, f, indent=4, ensure_ascii=False)
            f.close()

        path = '../txts/authors_fs/total_sentences.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for famous_sentence in famous_sentences:
                json.dump(famous_sentence, f, ensure_ascii=False)
                f.write('\n')
            f.close()


# 1 - 多进程爬虫 - 爬取和处理作品的类型
def pool_spider_works():
    work_filter = ['诗经', '乐府', '楚辞', '古文观止', '小学古诗',  # 过滤特殊类型的作品页面，后期处理
                   '初中古诗', '高中古诗', '小学文言文', '初中文言文',
                   '高中文言文', '唐诗三百首', '古诗三百首', '宋词三百首', '古诗十九首']

    work_types = []
    path = "../txts/works_types/all_types.txt"
    with open(path, 'r', encoding='utf-8') as f:
        work_type = f.readlines()
        f.close()

    for type in work_type:
        type = type.split('\n')[0]
        # if type not in work_filter:
        if type in work_filter:  # 爬取特殊的分类标签
            work_types.append(type)

    work_type_pages = {}
    for type in work_types:  # 提取每个类型对应所有作品的的网页 1-8  最多8页
        work_pages = []  # 注意每次更新
        for page in range(1, 9):
            target_url = "https://so.gushiwen.cn/shiwens/default.aspx?page=" \
                         + str(page) + "&tstr=" + type + "&astr=&cstr=&xstr="
            work_pages.append(target_url)

        work_type_pages[type] = work_pages

    # 使用多进程爬取
    for work_type, type_pages in work_type_pages.items():
        # if work_type not in ['清明节', '月亮', '写景', '写雪', '散文', '咏史', '怀古']:  # 重新访问
        #     continue
        print(work_type)
        spider = Spider()
        try:
            spider.type_name = work_type  # 类型名，便于保存
            for type_page in type_pages:
                spider.works_type_pages(type_page)

            # 写入数据
            path = '../txts/works_types/' + spider.type_name + '.txt'
            with open(path, 'w', encoding='utf-8') as f:
                for types in spider.work_types:
                    json.dump(types, f)
                    f.write('\n')
                f.close()

        except Exception as e:
            # 保存数据
            path = '../txts/works_types/' + spider.type_name + '.txt'
            with open(path, 'w', encoding='utf-8') as f:
                for types in spider.work_types:
                    json.dump(types, f)
                    f.write('\n')
                f.close()
            print("发生异常，注意查看————————", e)
            continue


# 2 - 爬取和处理作品的类型  特殊类型处理
def spider_works_special(page):
    spider = Spider()
    work_type = list(page.keys())[0]  # 作品的类型
    work_url = list(page.values())[0]  # 作品的url
    print('访问类型及页面为：', work_type + ' ' + work_url)

    # 加载所有作者名字
    path = '../jsons/authors_details/dynasty_of_author.json'
    with open(path, 'r', encoding='utf-8') as f:
        dynasty_of_author = json.load(f)
        f.close()

    try:
        html = spider.parser_url(work_url)  # 获取解析后的网页

        # 解析该类型包含的作品（title, author, dynasty, type）
        works = html.xpath('//div[@class="main3"]//div[@class="sons"]//span/a/text()')  # 根据div分组
        authors = html.xpath('//div[@class="main3"]//div[@class="sons"]//span/text()')  # 根据div分组

        no_author_works = ["江南", "守株待兔", "精卫填海", "王戎不取道旁李", "囊萤夜读", "古人谈读书"
            , "自相矛盾", "伯牙鼓琴", "学弈", "长歌行", "采薇(节选)", "迢迢牵牛星", "十一月四日风雨大作·其二",
                           " 《论语》十二章"
            , "司马光", "木兰诗", "庭中有奇树", "庄子与惠子游于濠梁之上", "酬乐天扬州初逢席上见赠", "鱼我所欲也",
                           "唐雎不辱使命", "邹忌讽齐王纳谏", "十五从军征", "芣苢", "静女",
                           "涉江采芙蓉", "子路、曾皙、冉有、公西华侍坐", "齐桓晋文之事", "论语十二章", "无衣",
                           "氓", "孔雀东南飞并序", "同从弟销南斋玩月忆山阴", "定风波(苏轼)", "鹧鸪天·座中有眉山隐客史",
                           "破阵子·为陈同甫赋壮词以寄", "闻王昌龄左迁龙标遥有此寄", "点绛唇·绍兴乙卯登绝顶小亭",
                           "水调歌头·送章德茂大卿使虏", "太常引·建康中秋夜为吕叔潜赋"
            , "登柳州城楼寄漳汀封连四州", "临江仙·夜登小阁忆洛中旧游"]
        i = 0
        j = 0
        page_of_works = []
        works_len = len(works)
        while i < works_len:
            work = str(works[i])
            type_of_work = {}

            if work in no_author_works:
                type_of_work["title"] = work
                type_of_work["author"] = None
                type_of_work["dynasty"] = None
                type_of_work["type"] = work_type
                print("work: ", work)
                print("author: ", "-----------------------------")
                i += 1  # 只加 作品
                page_of_works.append(type_of_work)
                continue

            if '(' in authors[j]:  # 作者处理
                author = authors[j].split('(')[1].split(')')[0]
            else:
                author = authors[j].split('《')[1].split('》')[0]  # 针对 《诗经》

            type_of_work["title"] = work
            type_of_work["author"] = author
            print("work: ", work)
            print("author: ", author)

            if author in dynasty_of_author:
                type_of_work["dynasty"] = dynasty_of_author[author]
            else:
                type_of_work["dynasty"] = None

            type_of_work["type"] = work_type
            i += 1
            j += 1

            page_of_works.append(type_of_work)

        path = '../txts/works_types/' + work_type + '.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for types in page_of_works:
                json.dump(types, f, ensure_ascii=False)
                f.write('\n')
            f.close()

        path = '../jsons/works_types/' + work_type + '.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(page_of_works, f, indent=4, ensure_ascii=False)
            f.close()

    except Exception as e:
        # # 保存数据
        # path = '../txts/works_types/' + spider.type_name + '.txt'
        # with open(path, 'w', encoding='utf-8') as f:
        #     for types in spider.work_types:
        #         json.dump(types, f)
        #         f.write('\n')
        #     f.close()
        print("发生异常，注意查看————————", e)
        print('！！！！发生异常的网页是：' + work_url)


# 2 - 多进程爬取
def pool_spider_works_special():
    work_type_pages = {
        "乐府": "https://so.gushiwen.cn/gushi/yuefu.aspx",
        "楚辞": "https://so.gushiwen.cn/gushi/chuci.aspx",
        "小学古诗": "https://so.gushiwen.cn/gushi/xiaoxue.aspx",
        "初中古诗": "https://so.gushiwen.cn/gushi/chuzhong.aspx",
        "高中古诗": "https://so.gushiwen.cn/gushi/gaozhong.aspx",
        "小学文言文": "https://so.gushiwen.cn/wenyan/xiaowen.aspx",
        "初中文言文": "https://so.gushiwen.cn/wenyan/chuwen.aspx",
        "高中文言文": "https://so.gushiwen.cn/wenyan/gaowen.aspx",
        "唐诗三百首": "https://so.gushiwen.cn/gushi/tangshi.aspx",
        "古诗三百首": "https://so.gushiwen.cn/gushi/sanbai.aspx",
        "宋词三百首": "https://so.gushiwen.cn/gushi/songsan.aspx",
    }

    # 使用多进程爬取
    all_pages = []
    for work_type, page in work_type_pages.items():
        tmp = {work_type: page}  # 创建字典
        all_pages.append(tmp)

    spider_works_special(all_pages[-1])
    # pool = Pool(7)  # 创建6个进程对象  本计算机 cpu 内核数量为8  print(cpu_count())
    # pool.map(spider_works_special, all_pages)


# 3 - 爬取和处理名句的类型 - 对应好名句的属性以及类型
def spider_sentences(sentence_type_pages, contents):
    for sentence_type, type_pages in sentence_type_pages.items():
        # if work_type not in ['清明节', '月亮', '写景', '写雪', '散文', '咏史', '怀古']:  # 重新访问
        #     continue
        print(sentence_type)
        spider = Spider()
        # spider.type_name = sentence_type  # 类型名，便于保存
        sentences_types = []  # 名句的类型
        famous_sentences = []  # 保存到文件
        sentences_type_urls = []
        try:
            for type_page in type_pages:
                print(type_page)
                html = spider.parser_url(type_page)  # 解析网页
                if html is None:  # 访问失败
                    print('注意: 此页没有数据！！！' + type_page + '\n')
                    continue

                # 解析该类型包含的作品（title, author, dynasty, type）
                sentences = html.xpath(
                    '//div[@class="main3"]/div[@class="left"]/div[@class="sons"]//a/text()')  # 根据div分组
                tmp_urls = html.xpath('//div[@class="main3"]/div[@class="left"]/div[@class="sons"]//a/@href')  # 对应的url

                sentences_len = len(sentences)
                if sentences_len == 0:
                    print('注意：此页后没有数据，' + type_page + '\n')
                    break

                # 判断是否有作者，某些是没有的，其次，名句朝代问题，后期处理
                # 写文件采用追加方式，后期与诗人的名句相整合
                # 存储名句的属性、存储名句对应的类型
                # print(sentences)
                i = 0
                while i < sentences_len:
                    url = spider.domain + tmp_urls[i]  # 名句对应的 url

                    if i + 1 == sentences_len:
                        break
                    print(sentences[i + 1])
                    if '《' not in sentences[i + 1]:
                        print("________-----s-s--s")
                        i += 1  # 跳过此句
                        continue

                    author_title = sentences[i + 1].split('《')
                    if '《' in author_title[0]:  # 该名句没有作者
                        title = author_title[0].split('》')[0]
                        author = ''
                    else:
                        title = author_title[1].split('》')[0]
                        author = author_title[0]

                    content = sentences[i]  # 名句内容
                    # print(content)

                    sentence_and_url = author + '##' + content + '##' + title + '##' + url + '\n'
                    tmp_sentence_type = {'title': title, 'content': content, 'type': sentence_type}
                    famous_sentence = {'title': title, 'author': author, 'dynasty': None,
                                       'content': content, 'translation': None,
                                       'annotation': None, 'appreciation': None}

                    sentences_types.append(tmp_sentence_type)
                    famous_sentences.append(famous_sentence)
                    sentences_type_urls.append(sentence_and_url)

                    i += 2  #

            # 将作品的类型与名句对应写入文件
            path1 = '../txts/sentences_types/' + sentence_type + '.txt'
            with open(path1, 'w', encoding='utf-8') as f:
                for sentence_types in sentences_types:
                    json.dump(sentence_types, f)
                    f.write('\n')
                f.close()

            # 将爬取的所有名句追加到文件
            path2 = '../txts/authors_fs/famous_sentence1.txt'
            with open(path2, 'a', encoding='utf-8') as f:
                for famous_sentence in famous_sentences:
                    if famous_sentence['content'] in contents:
                        continue
                    json.dump(famous_sentence, f)
                    f.write('\n')
                f.close()

            # 将爬取的所有的名句对应的 url 追加写入文件
            path3 = '../txts/sentences_types_urls/' + sentence_type + '.txt'
            with open(path3, 'a', encoding='utf-8') as f:
                for sentences_type_url in sentences_type_urls:
                    f.write(sentences_type_url)
                f.close()

            time.sleep(1)

        except Exception as e:
            # 将作品的类型与名句对应写入文件
            path1 = '../txts/sentences_types/' + sentence_type + '.txt'
            with open(path1, 'w', encoding='utf-8') as f:
                for sentence_types in sentences_types:
                    json.dump(sentence_types, f)
                    f.write('\n')
                f.close()

            # 将爬取的所有名句追加到文件
            path2 = '../txts/authors_fs/famous_sentence1.txt'
            with open(path2, 'a', encoding='utf-8') as f:
                for famous_sentence in famous_sentences:
                    json.dump(famous_sentence, f)
                    f.write('\n')
                f.close()

            # 将爬取的所有的名句对应的 url 追加写入文件
            path3 = '../txts/sentences_types_urls/' + sentence_type + '.txt'
            with open(path3, 'a', encoding='utf-8') as f:
                for sentences_type_url in sentences_type_urls:
                    f.write(sentences_type_url)
                f.close()

            print("\n发生异常，注意查看————————", e)
            print("此异常发生的类型为：", sentence_type + '\n')
            continue


# 3 - 多进程爬虫 - 处理爬取的名句（从类型处获取）
def pool_spider_sentences():
    sentence_types = []
    path = "../txts/sentences_types/all_types.txt"
    with open(path, 'r', encoding='utf-8') as f:
        sentence_type = f.readlines()
        f.close()

    for type in sentence_type:
        type = type.split('\n')[0]
        sentence_types.append(type)

    all_pages = []
    for sentence_type in sentence_types:  # 提取每个类型对应所有作品的的网页 1-8  最多8页
        if sentence_type not in ['读书', '励志', '哲理', '山水', '左传']:
            continue

        sentence_type_pages = {}
        sentence_pages = []  # 注意每次更新
        for page in range(1, 11):  # 名句可爬 10 页
            target_url = "https://so.gushiwen.cn/mingjus/default.aspx?page=" \
                         + str(page) + "&tstr=" + sentence_type + "&astr=&cstr=&xstr="
            sentence_pages.append(target_url)

        sentence_type_pages[sentence_type] = sentence_pages  # 字典： '春天'：['url1', 'url2']
        all_pages.append(sentence_type_pages)

    contents = []
    path = '../txts/authors_fs/famous_sentence1.txt'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:  # 每行都是名句
            sentence = json.loads(line)
            contents.append(sentence['content'])

    # 处理 BUG
    for pages in all_pages:  # 字典，各个类型的字典形式表示
        spider_sentences(pages, contents)

    # pool = Pool(6)  # 创建6个进程对象  本计算机 cpu 内核数量为8  print(cpu_count())
    # pool.map(spider_sentences, all_pages)


# 4 - 爬取和处理名句的类型 - 对应好名句的属性以及类型
def spider_sen_from_author(sentence_pages):
    for author, author_pages in sentence_pages.items():
        # if author not in ['清明节', '月亮', '写景', '写雪', '散文', '咏史', '怀古']:  # 重新访问
        #     continue
        print(author)
        spider = Spider()

        famous_sentences = []  # 保存到文件
        author_sentences_urls = []
        dynasty_of_author = author_pages[0]  # 作者的朝代
        try:
            for author_page in author_pages[1:]:
                print(author_page)
                html = spider.parser_url(author_page)  # 解析网页
                if html is None:  # 访问失败
                    print('注意: 此页没有数据！！！' + author_page + '\n')
                    continue

                # 解析该类型包含的作品（title, author, dynasty, type）
                sentences = html.xpath(
                    '//div[@class="main3"]/div[@class="left"]/div[@class="sons"]//a/text()')  # 根据div分组
                tmp_urls = html.xpath('//div[@class="main3"]/div[@class="left"]/div[@class="sons"]//a/@href')  # 对应的url

                sentences_len = len(sentences)
                if sentences_len == 0:
                    print('注意：此网页后没有数据，' + author_page + '\n')
                    break

                # 判断是否有作者，某些是没有的，其次，名句朝代问题，后期处理
                # 写文件采用追加方式，后期与诗人的名句相整合
                # 存储名句的属性、存储名句对应的类型
                # print(sentences)
                i = 0
                while i < sentences_len:
                    url = spider.domain + tmp_urls[i]  # 名句对应的 url

                    if i + 1 == sentences_len:
                        break

                    if '《' not in sentences[i + 1]:  # 没有写明作者及来处，跳过
                        print("此句没有标明出处，跳过。！！！" + sentences[i])
                        i += 1  # 跳过此句
                        continue

                    content = sentences[i]  # 名句内容
                    author_title = sentences[i + 1].split('《')
                    title = author_title[1].split('》')[0]
                    # author = author_title[0]

                    sentence_and_url = author + '##' + content + '##' + title + '##' + url + '\n'
                    famous_sentence = {'title': title, 'author': author, 'dynasty': dynasty_of_author,
                                       'content': content, 'translation': None,
                                       'annotation': None, 'appreciation': None}

                    famous_sentences.append(famous_sentence)
                    author_sentences_urls.append(sentence_and_url)

                    i += 2

            # 将爬取的所有名句追加到文件 - 以 json 文件保存
            path = '../jsons/authors_fs/famous_sentence2.json'
            with open(path, 'a', encoding='utf-8') as f:
                json.dump(famous_sentences, f, indent=4, ensure_ascii=False)  # 缩进的空格数，设置为非零值时，就起到了格式化的效果，比较美观
                f.close()

            # 将爬取的所有名句追加到文件 - 以文本文件保存
            path = '../txts/authors_fs/famous_sentence2.txt'
            with open(path, 'a', encoding='utf-8') as f:
                for famous_sentence in famous_sentences:
                    # if famous_sentence['content'] in contents:
                    #     continue
                    json.dump(famous_sentence, f, indent=4, ensure_ascii=False)  # 缩进的空格数，设置为非零值时，就起到了格式化的效果，比较美观
                    f.write('\n')
                f.close()

            # 将爬取的所有的名句对应的 url 追加写入文件
            path = '../txts/authors_fs_urls/' + author + '.txt'
            with open(path, 'w', encoding='utf-8') as f:
                for sentences_type_url in author_sentences_urls:
                    f.write(sentences_type_url)
                f.close()
            time.sleep(1)

        except Exception as e:
            # 将爬取的所有名句追加到文件 - 以 json 文件保存
            path = '../jsons/authors_fs/famous_sentence2.json'
            with open(path, 'a', encoding='utf-8') as f:
                json.dump(famous_sentences, f, indent=4, ensure_ascii=False)  # 缩进的空格数，设置为非零值时，就起到了格式化的效果，比较美观
                f.close()

            # 将爬取的所有名句追加到文件 - 以文本文件保存
            path = '../txts/authors_fs/famous_sentence2.txt'
            with open(path, 'a', encoding='utf-8') as f:
                for famous_sentence in famous_sentences:
                    # if famous_sentence['content'] in contents:
                    #     continue
                    json.dump(famous_sentence, f, indent=4, ensure_ascii=False)  # 缩进的空格数，设置为非零值时，就起到了格式化的效果，比较美观
                    f.write('\n')
                f.close()

            # 将爬取的所有的名句对应的 url 追加写入文件
            path = '../txts/authors_fs_urls/' + author + '.txt'
            with open(path, 'w', encoding='utf-8') as f:
                for sentences_type_url in author_sentences_urls:
                    f.write(sentences_type_url)
                f.close()

            print("\n发生异常，注意查看————————", e)
            print("此异常发生的作者为：", author + '\n')
            continue


# 4 - 多进程爬虫 - 处理爬取的名句（从作者处获取）
def pool_spider_sen_from_author():
    authors = []
    path = "../txts/authors_famous_sentences.txt"
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            authors.append(line.split('##')[0])  # 获取作者名字
        f.close()

    # 获取作者的朝代，便于后续属性存储
    path = '../jsons/authors_details/dynasty_of_author.json'
    with open(path, 'r', encoding='utf-8') as f:
        authors_and_dynasty = json.load(f)
        f.close()

    all_pages = []  # 使用队列，便于多进程爬取 形式：[{'李白'：['url1', 'url2']}, '杜甫'：['url1', 'url2']]
    for author, dynasty in authors_and_dynasty.items():  # 提取每个类型对应所有作品的的网页 1-10  最多10页
        # if author not in authors:  # 说明作者没有名句
        #     continue

        authors_pages = {}
        author_pages = [dynasty]  # 将作者的朝代传过去，便于更新属性
        for page in range(1, 11):  # 名句可爬 10 页
            target_url = "https://so.gushiwen.cn/mingjus/default.aspx?page=" \
                         + str(page) + "&tstr=&astr=" + author + "&cstr=&xstr="
            author_pages.append(target_url)

        authors_pages[author] = author_pages  # 字典： '春天'：['url1', 'url2']
        all_pages.append(authors_pages)

    # contents = []
    # path = '../txts/authors_fs/famous_sentence1.txt'
    # with open(path, 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    #     for line in lines:  # 每行都是名句
    #         sentence = json.loads(line)
    #         contents.append(sentence['content'])

    pool = Pool(8)  # 创建6个进程对象  本计算机 cpu 内核数量为8  print(cpu_count())
    pool.map(spider_sen_from_author, all_pages)


# 6 - 多进程爬虫 - 从其他网站获取 作者和朝代
def pool_get_dynasty_of_author():
    urls = []
    for i in range(2, 723):
        "http://www.gudianmingzhu.com/zuozhe/index_2.html"
        urls.append("http://www.gudianmingzhu.com/zuozhe/index_" + str(i) + ".html")
    spider = Spider()

    pool = Pool(7)  # 创建6个进程对象  本计算机 cpu 内核数量为8  print(cpu_count())
    pool.map(spider.author_and_dynasty, urls)


# 7 - 获取作者的合称
def get_collective_title(url_title):
    url = url_title[0]  # 对应的 url
    title = url_title[1]  # 作者的合称

    spider = Spider()
    html = spider.parser_url(url)
    dynasty_names = html.xpath('//p[@class="card-title"]')

    all_collective_title = []
    for dynasty_name in dynasty_names:
        dynasty = dynasty_name.xpath('./a/text()')[0]  # 作者朝代
        name = dynasty_name.xpath('./a/text()')[1]  # 作者名字
        print(name, dynasty)

        tmp = {
            "author": name,
            "dynasty": dynasty,
            "title": title
        }

        all_collective_title.append(tmp)

    path = "../txts/collective_title/author_collective_title.txt"
    with open(path, 'a', encoding='utf-8') as f:
        for c_t in all_collective_title:
            json.dump(c_t, f, ensure_ascii=False)
            f.write('\n')
        f.close()


# 7 - 多进程爬虫 - 获取作者的合称
def pool_get_collective_title():
    spider = Spider()
    spider.domain = "https://www.xungushici.com"
    html = spider.parser_url("https://www.xungushici.com/authors")  # 获取合称
    urls = html.xpath('//div[@id="divHeCheng"]//li[@class="m-1 badge badge-light"]')

    path = "../txts/collective_title/collective_title.txt"  # 作者的合称
    write_title = open(path, 'a', encoding='utf-8')

    url_collective_name = []
    for url in urls:
        tmp_url = spider.domain + url.xpath('./a/@href')[0]
        name = url.xpath('./a/text()')[0]

        write_title.write(name + '\n')

        print(tmp_url, name)
        tmp = [tmp_url, name]
        url_collective_name.append(tmp)  # 合称和url

    write_title.close()

    pool = Pool(8)  # 创建6个进程对象  本计算机 cpu 内核数量为8  print(cpu_count())
    pool.map(get_collective_title, url_collective_name)


# 9 - 多进程处理数据 - 将相同作者的作品对齐
def pool_align_author_works():
    path = '../jsons/tmp_process/repeated_authors.txt'
    with open(path, 'r', encoding='utf-8') as f:
        repeated_authors = f.readlines()
        f.close()

    root = '../completion_authors_works/identical_author/'
    for folder_path, folder_name, file_names in os.walk(root):
        author_names = [i.split('.')[0] for i in file_names]
        # sentences_types = [root + i for i in file_names]
        break

    repeated_authors = [i.split('\n')[0] for i in repeated_authors]

    authors = set(repeated_authors) - set(author_names)

    c_d = Clean_Data()
    # c_d.compare_author_work("李白")
    pool = Pool(7)  # 创建6个进程对象  本计算机 cpu 内核数量为8  print(cpu_count())
    pool.map(c_d.compare_author_work, authors)


# 10 - 作品包含名句
def work_include_sentence(work):
    path = '../data_nodes/node_famous_sentence.json'
    with open(path, 'r', encoding='utf-8') as f:
        sentences = json.load(f)
        f.close()

    author = work['author']

    content = work['content']
    content = content.replace("：", "，").replace("“", "，").replace("”", "，").replace("‘", "，").replace("；", "，"). \
        replace("’", "，").replace("。", "，").replace("！", "，").replace("？", "，").replace("\n", "，")
    content = set(content.split("，"))

    include = []
    flag = False
    for sentence in sentences:
        tmp_author = sentence['author']

        tmp_content = sentence['content']
        tmp_content = tmp_content.replace("：", "，").replace("“", "，").replace("”", "，").replace("‘", "，").replace("；",
                                                                                                                  "，"). \
            replace("’", "，").replace("。", "，").replace("！", "，").replace("？", "，").replace("\n", "，")
        tmp_content = set(tmp_content.split("，"))

        and_len = len(content & tmp_content)  # 交集个数
        if and_len >= 2:
            if author == tmp_author:
                include.append(sentence['content'])  # 包括名句
                flag = True

            else:
                print("！！！作者不同，", sentence)

    if not flag:
        print("？？？？该作品没有名句，", work)

    work_content = {
        "title": work['title'],
        "author": work['author'],
        "dynasty": work['dynasty'],
        "content": work['content'],
        "translation": None,
        "annotation": None,
        "background": None,
        "appreciation": None,
        "include": include
    }

    path = '../data_nodes/node_tmp_work_content.txt'
    with open(path, 'a', encoding='utf-8') as f:
        json.dump(work_content, f, ensure_ascii=False)
        f.write('\n')
        f.close()


# 10 - 多进程处理，作品包含的名句
def pool_work_include_sentence():
    path = '../data_nodes/node_work_content.json'
    with open(path, 'r', encoding='utf-8') as f:
        contents = json.load(f)
        f.close()

    # work_include_sentence(contents[50])
    pool = Pool(8)  # 创建8个进程对象 print(cpu_count())
    pool.map(work_include_sentence, contents)


# 20 - 获取所有数据
def access_data():
    # 1、数据获取部分
    spider = Spider()
    # spider.update_data()  # 更新朝代和作者的数据
    # spider.update_author_works()   # 更新作者的作品和名句
    # spider.update_work_sen_types()  # 更新 作品和名句 的类型

    # url = "http://www.gudianmingzhu.com/zuozhe/index.html"
    # spider.author_and_dynasty(url)  # 获取作者对应的朝代

    # 2 - 多进程爬虫 - 爬取和处理作品的类型
    # pool_spider_works()

    # 3 - 多进程爬虫 - 爬取和处理名句的类型
    # pool_spider_sentences()

    # 4 - 多进程爬虫 - 爬取和处理名句(作者处获取)
    # pool_spider_sen_from_author()

    # 5 - 多进程爬虫 - 爬取 作者和朝代
    # pool_get_dynasty_of_author()

    # 6 - 多进程爬虫 - 爬取特殊的作品与类型
    # pool_spider_works_special()

    # 7 - 多进程爬虫 - 爬取各位作者的合称
    # pool_get_collective_title()

    # 8 - 多进程处理数据 - 合并相同作者的作品
    # pool_align_author_works()

    # 9 - 多进程合并所有作者的作品

    # 2、数据清洗部分
    clean_data = Clean_Data()
    # clean_data.process_authors_works()
    # clean_data.json_to_txt()
    # clean_data.dynasty_of_author()   # 将作者与朝代对应
    # clean_data.create_properties()  # 创建作品的属性值
    # clean_data.txt_to_json()  # 存储形式改变
    # clean_data.merge_famous_sentences()   #归并名句
    # clean_data.dynasties_of_authors()  # 计算每个朝代的作者
    # clean_data.unify_dynaty()  # 统一朝代
    # clean_data.completion_author_dynasty()
    # clean_data.get_author_nodes()  # 提取作者节点
    # clean_data.get_repeated_author_name()  # 获取重复名字
    # clean_data.copy_files()  # 复制文件
    # clean_data.merge_author_works()  # 合并作者的所有作品
    # clean_data.create_user_dict()
    # clean_data.get_author_total_works()  # 获取作者的所有作品
    # clean_data.get_work_title()  # 获取知名作者作品的标题
    clean_data.change_file()  # 将 json 文件转换成 csv 文件

    # 3、知识补全部分
    # knowledge_completion = Knowledge_Completion()
    # knowledge_completion.dynasty_compeltion()


if __name__ == '__main__':
    log_file_name = './log.txt'
    # 记录正常的 print 信息
    sys.stdout = Logger(log_file_name)
    access_data()
