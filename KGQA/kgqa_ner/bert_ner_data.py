# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/11 8:04
 @Author: Glimmering
 @Function: 处理命名实体识别的数据
"""
import json
import os
import random
import sys
import numpy as np
import loguru


# 1 - 从诗人的简介进行命名实体识别 ———— 弃用
def poet_profile():
    path = './user_dict/dict_category/dict_author_sorted_work.txt'
    author_top_500 = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines()[:300]:
            author_top_500.append(line.split('\n')[0])  # 仅使用前 3000 个作者的简介
        f.close()

    authors = []
    root = "D:/5.2_py_fs/cd_1/作者/"
    for _, folder_names, file_names in os.walk(root):
        for folder_name in folder_names:
            author = folder_name.split('的')[0]
            if author in author_top_500:
                # print(author)
                authors.append(author)
        break

    write_path = '../model_label/bert_label/author_profile.txt'  # 最长文本长度为 400
    ap_file = open(write_path, 'w', encoding='utf-8')
    for author in authors:  # 获取所有简介
        path = root + author + '的简介/' + author + '的简介.txt'
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines()[1:]:
                if len(line) <= 10:
                    continue

                idx = line.find(':')
                # line = author + '，' + line[idx + 2:]
                line = line[idx + 2:]
                # print(line, end='')
                ap_file.write(line)
            f.close()

    ap_file.close()


# 2 - 将打了标签的数据转换成特定的格式数据集
def change_label_data():
    global type
    # path = '../model_label/bert_label/export_0.json'   # 从label-studio平台导出的数据
    # path = '../model_label/bert_label/export_1.json'
    path = '../model_label/bert_label/export_2.json'
    with open(path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
        f.close()

    # 以简单内容（JSON——MIN）导出的 json 文件，以这种方式转换
    dataset_labels = []
    for label_data in data_list:
        if len(label_data) == 8:
            text = label_data['text']  # 原文本
            labels = label_data['label']  # 注意，不是每一问句都有label，需要特殊处理

            entities = []  # 所有实体
            for label in labels:
                start_idx = label['start']  # 标注开始点和结束点
                end_idx = label['end']
                entity = label['text']

                if len(label['labels']) > 1:  # 有多个标签
                    types = label['labels']
                    for type in types:
                        entities.append({
                            "start_idx": start_idx,
                            "end_idx": end_idx,
                            "type": type,
                            "entity": entity
                        })
                else:
                    type = label['labels'][0]  # 只有一个标签
                    entities.append({
                        "start_idx": start_idx,
                        "end_idx": end_idx,
                        "type": type,
                        "entity": entity
                    })

            # 整个标记完的数据集
            dataset_labels.append({
                "text": text,
                "entities": entities
            })

        else:   # 该问句没有实体
            text = label_data['text']  # 原文本
            # 整个标记完的数据集
            dataset_labels.append({
                "text": text,
                "entities": []
            })

    # 以详细内容（JSON）导出的 json 文件，以下列这种方式转换
    """
    dataset_labels = []
    for label_data in data_list:
        text = label_data['data']['text']  # 原文本
        labels = label_data['annotations'][0]['result']

        entities = []  # 所有实体
        for label in labels:
            value = label['value']
            start_idx = value['start']  # 标注开始点和结束点
            end_idx = value['end']
            entity = value['text']
            if len(value['labels']) > 1:  # 有多个标签
                types = value['labels']
                for type in types:
                    entities.append({
                        "start_idx": start_idx,
                        "end_idx": end_idx,
                        "type": type,
                        "entity": entity
                    })
            else:
                type = value['labels'][0]  # 只有一个标签
                entities.append({
                    "start_idx": start_idx,
                    "end_idx": end_idx,
                    "type": type,
                    "entity": entity
                })

        # 整个标记完的数据集
        dataset_labels.append({
            "text": text,
            "entities": entities
        })
    """

    # path = '../model_label/bert_label/author_profile.json'
    # path = '../model_label/bert_label/ft_data_ner_0.json'
    # path = '../model_label/bert_label/ft_data_ner_1.json'
    path = '../model_label/bert_label/ft_data_ner_2.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dataset_labels, f, indent=2, ensure_ascii=False)
        f.close()


# 3 - 合并标注的数据（多次标注，根据自己的实际情况合并）
def merge_label_data():
    path = '../model_label/bert_label/ft_data_ner_0.json'
    with open(path, 'r', encoding='utf-8') as f:  # 第一次标注的数据
        labels = json.load(f)
        f.close()

    path = '../model_label/bert_label/ft_data_ner_1.json'
    with open(path, 'r', encoding='utf-8') as f:
        labels.extend(json.load(f))
        f.close()

    path = '../model_label/bert_label/ft_data_ner_2.json'
    with open(path, 'r', encoding='utf-8') as f:
        labels.extend(json.load(f))
        f.close()


    path = '../model_label/bert_label/ft_data_ner.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)
        f.close()


# 4 - 新增其它不相关的数据
def add_others_data():
    # root = '../model_label/bert_label/author_profile.json'
    root1 = '../model_label/bert_label/ft_data_ner.json'
    with open(root1, 'r', encoding='utf-8') as f:
        authors = json.load(f)
        f.close()

    root2 = '../model_label/bert_label/ft_data_others.txt'
    test_f = open(root2, 'w', encoding='utf-8')
    path = '../model_label/query_label/others_4.txt'
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines()[:4377]:  # 取部分数据
            test_f.write(line)
        f.close()
        test_f.close()

    with open(root2, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            authors.append({
                "text": line,
                "entities": []
            })
        f.close()

    with open(root1, 'w', encoding='utf-8') as f:
        json.dump(authors, f, indent=2, ensure_ascii=False)
        f.close()


# 5 - 拆分数据集
def split_dataset():
    # path = '../model_label/bert_label/author_profile.json'
    path = '../model_label/bert_label/ft_data_ner.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    cnt = 0
    train = []  # 训练集
    dev = []  # 验证集
    idxs = random.sample(range(0, 31100), 31100)  # 不重复的数字
    for idx in idxs:
        if cnt >= 26000:
            dev.append(data[idx])
        else:
            train.append(data[idx])
        cnt += 1

    path = '../model_label/bert_label/train_data.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(train, f, indent=2, ensure_ascii=False)
        f.close()

    path = '../model_label/bert_label/dev_data.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dev, f, indent=2, ensure_ascii=False)
        f.close()


# 20 - 使用 bert 模型进行 ner
def bert_ner():
    # poet_profile()  # 方式一
    # change_label_data()  # 规整化数据集
    # merge_label_data()
    # add_others_data()
    split_dataset()  # 划分数据集


if __name__ == "__main__":

    # bert_ner()
    path = '../model_label/bert_label/ft_data_ner.json'  # 27623 条源数据 + 4377条其他数据
    # path = '../model_label/bert_label/ft_data_ner_0.json'
    # path = '../model_label/bert_label/ft_data_ner_1.json'
    # path = '../model_label/bert_label/ft_data_ner_2.json'
    # path = '../model_label/bert_label/train_data.json'  # 26000 条数据
    # path = '../model_label/bert_label/dev_data.json' # 5000 条数据
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(len(data))

