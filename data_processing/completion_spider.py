"""
 coding=utf-8
 @Software: PyCharm
 @Date: 2024/3/22 15:41
 @Author: Glimmering
 @Function: 获取所有作者的诗词 进行诗词补全
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


# C - 1 爬取数据
class Spider:
    def __init__(self):
        self.domain = "https://www.shicimingju.com"

        self.headers = {'user-agent': UserAgent().random}
        self.type_name = ''  # 使用进程爬虫时，得到相应的名字
        self.work_types = []

        self.author = None

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
        # print('div——list', div_list)

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

                    # if title not in author_links:  # 判断是否有重复的名字
                    #     author_links[title] = [self.domain + link]  # 标题加链接
                    # else:
                    #     author_links[title].append(self.domain + link)

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
        root = '/作者/' + author + '的简介'  # 创建根目录

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

    # 9、爬取并存储每位作者的诗文
    def spider_and_store(self, url):
        html = self.parser_url(url)
        if html is None:  # 访问失败
            print('5 注意访问此网页失败 ！！！' + url)
            return False, []

        author_works = []
        works = html.xpath('//div[@class="shici_list_main"]')

        if not works:  # 此页面后没有数据了
            print('------注意，此页面后没有数据啦-----' + url)
            return False, author_works

        # 获取本页作者的所有作品
        for work in works:
            try:
                # ['《石灰吟》']
                title = work.xpath('./h3/a/text()')[0].split('《')[1].split('》')[0]

                # 处理作品的内容
                sentences = work.xpath('./div[@class="shici_content"]/text()')
                sentences1 = work.xpath('./div[@class="shici_content"]/div/text()')  # 展开全文的内容
                sentences.extend(sentences1)

                content = ""
                for sentence in sentences:
                    sentence = sentence.replace("\n", "").replace(" ", "")
                    if sentence:  # 将句子整合
                        content += sentence + '\n'

                author_work = {"title": title,
                               "author": self.author,
                               "dynasty": None,
                               "content": content,
                               "translation": None,
                               "annotation": None,
                               "background": None,
                               "appreciation": None
                               }
                # print(author_work)
                author_works.append(author_work)

            except Exception as e:
                print("6 ！！！发生异常：", e)
                print("6 发生异常的作者为：" + self.author + url)
                continue

        return True, author_works  # 作者所有的诗词

    # 10、完成作者所有作品的翻页
    def switch_pages(self, url):
        author_works_urls = []
        # https://www.shicimingju.com/chaxun/zuozhe/9.html
        number = url.split('/')[-1].split('.')[0]  # 提取目标网页页面

        for i in range(1, 500):  # 作者作品分页最大为 500
            author_works_urls.append("https://www.shicimingju.com/"
                                     "chaxun/zuozhe/" + str(number) + "_" + str(i) + ".html")

        author_works = []
        for author_works_url in author_works_urls:
            try:
                print("分页为：" + author_works_url)
                flag, tmp_author_works = self.spider_and_store(author_works_url)  # 爬取和存储作者的所有作品
                author_works.extend(tmp_author_works)  # 最后存储
                if not flag:  # 后续页面不再访问
                    break

            except Exception as e:
                print("4 异常为：", e)
                print("4 ！！！！发生异常！！！ 异常网页为：" + self.author + author_works_url)
                continue

        # 以 json 格式写入
        path = '../completion_authors_works/json/' + self.author + '.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(author_works, f, indent=4, ensure_ascii=False)
            f.close()

        # 以 txt 格式写入
        path = '../completion_authors_works/txt/' + self.author + '.txt'
        with open(path, 'w', encoding='utf-8') as f:
            for tmp in author_works:
                json.dump(tmp, f, ensure_ascii=False)
                f.write('\n')
            f.close()


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

        root = '../txts/works_types/'  # 转换 作品-类型 保存
        target_root = '../jsons/works_types/'

        # root = '../txts/authors_works/'  # 转换 作者-作品 保存
        # target_root = '../jsons/authors_works/'

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


# 7、补全所有诗人的作品
def completion_authors_works(page_url):
    spider = Spider()
    html = spider.parser_url(page_url)
    # print("总爬取的页面是 ！！！ " + page_url)
    if html is None:  # 访问失败
        print('1 注意: 此页没有数据！！！' + page_url)
        return

    # 解析本页面的所有作者
    authors_pages = html.xpath('//div[@class="zuozhe_list_item"]')  # 根据div分组
    if authors_pages is None:
        print('2 注意: 网页解析失败！！！' + page_url)
        return

    for author_page in authors_pages:  # 爬取本页面的所有作者
        try:
            author_url = spider.domain + author_page.xpath('./h3/a/@href')[0]  # 作者的作品网页链接
            spider.author = author_page.xpath('./h3/a/text()')[0].split(']')[-1]  # 作者
            if '?' in spider.author:
                spider.author = spider.author.replace("?", "-")
                print("爬取作者为 -- " + spider.author + ": " + author_url)
                spider.switch_pages(author_url)
                continue
            if '*' in spider.author:
                spider.author = spider.author.replace("*", "-")
                print("爬取作者为 -- " + spider.author + ": " + author_url)
                spider.switch_pages(author_url)
                continue

            print("爬取作者为 -- " + spider.author + ": " + author_url)
            spider.switch_pages(author_url)
        except Exception as e:
            print("3 异常为：", e)
            print("3 ！！！！发生异常！！！ 异常网页为：" + spider.author + page_url)
            continue


# 6 - 多进程爬虫 - 从其他网站获取 作者和朝代
def pool_completion_authors_works():
    urls = []
    for i in range(1, 653):
        urls.append("https://www.shicimingju.com/category/all_" + str(i))

    start_time = time.time()
    # spider.completion_authors_works(urls[0])

    pool = Pool(7)  # 创建7个进程对象  本计算机 cpu 内核数量为8  print(cpu_count())
    pool.map(completion_authors_works, urls)

    end_time = time.time()

    print("爬完所有页面的时间为：", end_time - start_time)


if __name__ == '__main__':
    url = "https://so.gushiwen.cn/authorv_b90660e3e492.aspx"
    spider = Spider()
    html = spider.parser_url(url)
    print(html.xpath('//div[@class="left"]//div[@class="contyishang"]//p/text()'))
    # pool_completion_authors_works()
