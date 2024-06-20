# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/11 23:27
 @Author: Glimmering
 @Function: 进行数据处理 - 生成用户字典、训练用户意图分类模型
"""

import json
import os
import sys

import jieba
import jieba.posseg

from logger import Logger
import pandas as pd


# 1 - 根据搜集的数据，生成用户词典，便于分词
def generate_user_dict():
    root = '../user_dict/dict_category/'

    file_names = ['dict_famous_sentence.txt', 'dict_sorted_title.txt',
                  'dict_author_sorted_work.txt', 'dict_collective_title.txt',
                  'dict_dynasty.txt', 'dict_work_type.txt']
    dict_path = [root + i for i in file_names]

    # 所有类型词典，生成总的用户词典
    user_dict = {}
    for path in dict_path:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.split('\n')[0] + ' ' + str(3) + ' ' + 'n' + '\n'  # 按照jieba分词字典的模式来
                if line not in user_dict:
                    user_dict[line] = 1
                else:
                    user_dict[line] += 1
            f.close()

    # 重复的较少：
    # a = sorted(user_dict.items(), key=lambda k: k[1], reverse=True)
    # print(a)

    path = '../user_dict/user_dict.txt'
    with open(path, 'w', encoding='utf-8') as f:
        for word, _ in user_dict.items():
            f.write(word)
        f.close()


# 2 - 提取知名作者（作品数量 >= 10）作品的标题
def extract_work_title():
    path = '../user_dict/dict_category/author_work_sorted.json'
    with open(path, 'r', encoding='utf-8') as f:
        author_sorted = json.load(f)
        f.close()

    work_titles = {}
    for author, work_cnt in author_sorted.items():  # 收录的作者作品数量大于等于10的有2525位
        if work_cnt < 10:
            break

        if "诗经" in author:
            continue

        path = '../data_nodes/node_works/' + author + '.json'
        with open(path, 'r', encoding='utf-8') as f:
            author_work = json.load(f)
            for work in author_work:  # 避免标题重复
                title = work['title']
                print(title)
                if title not in work_titles:
                    work_titles[title] = 1
                else:
                    work_titles[title] += 1

            f.close()

    tmp_dict = sorted(work_titles.items(), key=lambda k: k[1], reverse=True)

    work_titles = {}
    for work in tmp_dict:  # 以字典形式写到文件
        work_titles[work[0]] = work[1]

    path = '../user_dict/dict_category/dict_sortd_title.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(work_titles, f, indent=4, ensure_ascii=False)
        # for title in work_titles:
        #     print(title)
        #     f.write(title + '\n')
        f.close()


# 3 - 分词测试 - 基本通过
def cut_sentence():
    path = '../user_dict/user_dict.txt'
    jieba.load_userdict(path)  # 加载用户词典的时候，尽量放在文件第一次启动的地方

    # 进行词性标注的分词
    # sentence = "哈喽，明代诗词是中国文学史上的瑰宝，想知道那些创造了经典作品的诗人词人都是谁，你能告诉我吗？"
    # pt = jieba.posseg.POSTokenizer()
    #
    # print(pt.lcut(sentence))  # 得到 pair键值对，使用遍历取值
    # # print(jieba.posseg.cut(str)) # 作用一样
    # for i, k in pt.lcut(sentence):
    #     print(i, k)

    # 进行分词的整个流程可以形成一个类
    # path = './user_dict/stopwords/cn_stopwords.txt'  # 加载停用词
    # with open(path, 'r', encoding='utf-8') as f:
    #     stopwords = f.read().split('\n')
    #     f.close()

    # 1 - author_of_dynasty
    # sentence = "你能否告诉我明代都有哪些诗人词人，我很想了解他们的身份和成就。"
    # sentence = "哈喽，明代诗词是中国传统文化的重要载体，想知道那些在诗词史上留下浓墨重彩一笔的诗人词人都是谁，你能告诉我吗？"

    # 2 - c_t_of_author
    # sentence = "您能否科普一下古代被尊称为四大才女的女性都有谁？谢谢。"
    # sentence = "哈喽！您能否列举一下竹林七贤这七位在思想界颇具影响力的人物的姓名？"

    # 3 - dynasty_of_author
    # sentence = "我对苏轼所处的历史环境及其对他地方治理理念的影响极为关注，能否详述？"
    # sentence = "你能告诉我曹操是哪个时期的政治家、军事家和战略家？"

    # 4 - fs_of_author
    # sentence = "请问你是否洞悉李清照的诗词精髓？能否列举一些她的诗词名句以揭示其核心思想？"
    # sentence = "我对柳永的诗词艺术深感兴趣，作为一位著名词人，他有哪些广为人知的佳句？"

    # 5 - fs_of_dynasty
    # sentence = "你好！我很想知道五代时期有哪些诗词名句至今仍被学者们研究探讨？"
    # sentence = "你能给我推荐一些南北朝时期诞生的著名古诗词句子吗？"

    # 6 - fs_of_type
    # sentence = "描绘爱情百态的古典诗词名句是我此刻热切探寻的对象，能否指点一二？"
    # sentence = "有哪些诗文中的名句展现了读书与人生阅历、道德修养的密切关联？"

    # 7 - gender_of_author
    # sentence = "我很想探究古代女性在诗歌领域的贡献，可否介绍一些代表性的诗人？"
    # sentence = "你能否分享一下王维的性别信息？他是男诗人还是女诗人？"

    # 8 - work_of_author
    # sentence = "嗨，李煜的词作深情款款，感人肺腑，想知道他究竟留下了哪些词作供后人品味，你能列举一下吗？"
    # sentence = "杜甫的诗歌是中华文化的瑰宝，我渴望深入了解他的全部作品，请问具体有哪些？"

    # 9 - work_of_dynasty
    # sentence = "我对隋代的诗词名篇有着浓厚的兴趣，能否请你告诉我一些代表作品？感激不尽。"
    # sentence = "明代应该有很多著名的诗词作品，你能列举出来吗？"

    # 10 - work_of_type
    # sentence = "你能告诉我一些古诗词中对中秋节美好祝愿的表达吗？"
    sentence = "我很想知道，有哪些古代诗词以雨为象征，探讨了人性的复杂或矛盾的深度诗篇？"

    # segment = ' '.join(jieba.cut(sentence))
    print("原句：" + sentence)

    # segment_list = jieba.lcut(sentence)   # 生成的是切分好的列表
    # segment = []
    # for seg in segment_list:
    #     if seg not in stopwords:
    #         segment.append(seg)
    # print("分词后的句子为：" + ' '.join(segment))

    print("分词后的句子为：" + ' '.join(jieba.cut(sentence)))


# 4 - 问句规整化 - 除去相同的问句和空行
def order_data():
    root = '../model_label/fasttext_label/'
    label_name = {}
    for folder_path, folder_name, file_names in os.walk(root):
        for file in file_names:
            label = file.split('.')[0]  # 获取 label 名称
            label_name[label] = root + file  # 该标签下的数据
        break

    path = '../model_label/query_label/'
    for label, root in label_name.items():
        sentences = {}
        t_root = path + label + '.txt'
        f_t = open(t_root, 'w', encoding='utf-8')
        with open(root, 'r', encoding='utf-8') as f:
            for sentence in f.readlines():
                if len(sentence) == 1:
                    continue

                if sentence not in sentences:
                    sentences[sentence] = 1
                else:
                    sentences[sentence] += 1

            for sentence, cnt in sentences.items():
                # print(sentence, cnt)
                f_t.write(sentence)

            f_t.close()
            f.close()


# 5 - 生成带标签的数据集
def generate_dataset():
    path = '../user_dict/user_dict.txt'
    jieba.load_userdict(path)  # 加载用户词典的时候，尽量放在文件第一次启动的地方

    label_name = {}
    root = './query_label/'
    for folder_path, folder_name, file_names in os.walk(root):
        for file in file_names:
            label = file.split('.')[0]  # 获取 label 名称
            label_name[label] = root + file  # 该标签下的数据
        break

    # 过滤停用词 - 不过滤停用词的效果更好
    # path = './user_dict/stopwords/cn_stopwords.txt'
    # with open(path, 'r', encoding='utf-8') as f:
    #     stopwords = [line.split('\n')[0] for line in f.readlines()]
    #     f.close()

    # 提取数据，生成数据集
    sentences = []
    seg_sentences = []
    labels = []
    for label, path in label_name.items():
        with open(path, 'r', encoding='utf-8') as f:
            print(path)
            for line in f.readlines():
                sentence = line.replace('\n', '')
                sentences.append(sentence)  # 原问句

                # seg_sentence = ''
                # for word in jieba.lcut(sentence):
                #     if word not in stopwords:
                #         seg_sentence += ' ' + word  # 切分后的问句
                seg_sentence = ' '.join(jieba.cut(sentence))

                seg_sentences.append(seg_sentence)

                labels.append(label)  # 该问句的标签

    df = pd.DataFrame({"sentence": sentences, "seg_sentence": seg_sentences, "label": labels})
    # path = '../dataset/unfiltered_stopwords/dataset.xlsx'  # 未过滤停用词
    path = './dataset/dataset.xlsx'
    df.to_excel(path, sheet_name='Sheet1', startcol=0, index=False)


# 20 - 处理杂项数据，汇总数据
def process():
    path = '../model_label/query_label/dynasty_of_author.txt'
    with open(path, 'r', encoding='utf-8') as f:
        all_data = f.readlines()
        f.close()

    path = '../model_label/query_label/tmp_author.txt'
    author_f = open(path, 'w', encoding='utf-8')
    for data in all_data:
        data = data.split(' ')[1]
        # print(data)
        author_f.write(data)

    author_f.close()


if __name__ == "__main__":
    log_file_name = './log.txt'
    # 记录正常的 print 信息
    sys.stdout = Logger(log_file_name)

    # process()
    # extract_work_title()  # 抽取作品的标题
    generate_user_dict()  # 生成用户词典
    # cut_sentence()  # 分词测试
    # order_data()  # 规整数据
    # generate_dataset()  # 生成模型的数据集

    # sentence = "我好喜欢这句诗：“山气日夕佳，飞鸟相与还。你喜欢吗？小诗”"
    # path = './user_dict/user_dict.txt'
    # jieba.load_userdict(path)  # 加载用户词典的时候，尽量放在文件第一次启动的地方
    #
    # cut_sentence = ' '.join(jieba.cut_for_search(sentence))
    # print(cut_sentence)


