# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/12 19:45
 @Author: Glimmering
 @Function: 使用 fasttext 对用户的问句进行意图识别和分类
"""

import os
import sys

import pandas as pd
import fasttext as ft
from fasttext import train_supervised
from sklearn.metrics import classification_report  # 混淆矩阵
from sklearn.model_selection import train_test_split  # 数据划分 - k-折交叉验证
import jieba
from loguru import logger


# 1 - 设置模型参数池
def params_pool():
    keys = ['lr', 'epoch', 'wordNgrams', 'dim', 'minCount', 'minn', 'maxn', 'bucket', 'loss', 'pretrainedVectors']
    params_setting_list = [
        [0.3, 20, 4, 300, 10, 1, 3, 500000, 'softmax'],
        [0.3, 10, 4, 300, 10, 1, 3, 500000, 'softmax'],
        [0.1, 10, 4, 300, 10, 1, 3, 500000, 'softmax'],
    ]
    params_list = [dict(zip(keys, values)) for values in params_setting_list]
    return params_list


# 2 - 将sentence 和 label 组装成 fastText 训练的特定格式
def train_data_format(X, Y, label='__label__'):
    data_set = []
    for sent, lab in zip(X, Y):  # X 为训练数据，y为训练数据的标签
        try:
            data_set.append(label + str(lab) + ' ' + sent)
        except:
            print(sent, lab)
    return data_set


# 3 - 拆分带标签的数据为句子列表和标签列表
def split_sent_and_label(path):
    sents, labels = [], []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            label, sent = line.split(' ', 1)
            label = label.replace('__label__', '')
            sents.append(sent)
            labels.append(label)

    return sents, labels


# 4 - 将拆分后的数据集写入对应的文件
def write_list_into_file(object, path):
    with open(path, 'w', encoding='utf-8') as f:
        for line in object:
            f.write(line + '\n')


# 5 - 对数据集进行拆分，得到训练集、验证集和测试集
def dataset_split(dataset, path):
    df = pd.read_excel(dataset, sheet_name="Sheet1")
    X = df['seg_sentence'].tolist()  # 分好词的句子
    y = df['label'].tolist()  # 分类标签

    # 拆分训练、验证、测试集
    # test_size = 0.2   常见比例是3:1
    X_train_dev, X_test, y_train_dev, y_test = train_test_split(X, y, test_size=0.1)
    X_train, X_dev, y_train, y_dev = train_test_split(X_train_dev, y_train_dev, test_size=0.1)

    # 将训练数据与标签组装
    train_data = train_data_format(X_train, y_train)
    test_data = train_data_format(X_test, y_test)
    dev_data = train_data_format(X_dev, y_dev)

    # 写入文件
    write_list_into_file(train_data, path + 'train_data.txt')
    write_list_into_file(test_data, path + 'test_data.txt')
    write_list_into_file(dev_data, path + 'dev_data.txt')


# 6 - 训练模型、测试和输出各意图PRF值
def fasttext_train(train_data, test_data, model_path, **kwargs):
    # 训练
    clf = train_supervised(input=train_data, **kwargs)  # **kwargs 训练参数列表
    clf.save_model('%s.bin' % model_path)

    # 测试
    result = clf.test(test_data)
    precision = result[1]
    recall = result[2]
    # print('Precision: {0}, Recall: {1}\n'.format(precision, recall))
    logger.info('Precision: {0}, Recall: {1}\n'.format(precision, recall))
    # 输出每类PRF值
    test_sents, y_true = split_sent_and_label(test_data)
    y_pred = [i[0].replace('__label__', '') for i in clf.predict(test_sents)[0]]
    logger.info(classification_report(y_true, y_pred, digits=3))
    # print(classification_report(y_true, y_pred, digits=3))


# 7 - 测试模型并输出各类意图的PRF值
def model_test(test_file, model_path):
    logger.info("模型测试……")
    clf = ft.load_model(model_path)
    test_sents, y_true = split_sent_and_label(test_file)
    y_pred = [i[0].replace('__label__', '') for i in clf.predict(test_sents)[0]]
    # 输出各类标签的PRF值
    tmp_cr = classification_report(y_true, y_pred, digits=3)
    # print(tmp_cr)

    logger.info(tmp_cr)


# 8 - 模型预测，预测句子label
def model_predict(sent_list, model_path):
    clf = ft.load_model(model_path)
    # 预测结果
    topN = 3  # 返回最可能的三种情况
    res = clf.predict(sent_list, k=topN)  # , threshold=0.3
    # 预测标签
    y_pred = [[lab.replace('__label__', '') for lab in labs] for labs in res[0]]
    # 预测概率
    y_prob = [[p for p in probs] for probs in res[1]]
    # 组装topN的预测结果
    topN_pred = list(zip(y_pred, y_prob))
    return topN_pred


# 9 - 模型流水线
def model_pipeline():
    # 注意：训练和测试部分是1-4，预测部分是5

    # 1 - 拆分训练、验证、测试集
    path = './dataset/'  # 没有过滤停用词

    dataset = './dataset/dataset.xlsx'  # 没有过滤停用词
    print("拆分数据集……")
    dataset_split(dataset, path)

    # 2 - 训练模型
    print("模型训练中……")
    root = '../models/fasttext_model'  # 如果相对路径报错，请采用绝对路径
    # 根据实际情况进行参数设置,防止欠拟合或过拟合，  wordNgrams = 4
    # kwargs = {'lr': 0.4, 'epoch': 10, 'wordNgrams': 4, 'dim': 300, 'minCount': 10, 'minn': 1, 'maxn': 3,
    #           'bucket': 500000, 'loss': 'softmax'}

    kwargs = {'lr': 0.1, 'epoch': 50, 'wordNgrams': 3, 'dim': 300, 'minCount': 10, 'minn': 1, 'maxn': 3,
              'bucket': 500000, 'loss': 'softmax'}

    # 没有过滤停用词的训练
    t_path = './dataset/train_data.txt'
    d_path = './dataset/dev_data.txt'

    fasttext_train(t_path, d_path, root, **kwargs)
    print("模型训练完成……")

    model_path = '../models/fasttext_model.bin'
    # 4 - 测试集 - 对模型进行测试
    t_path = './dataset/test_data.txt'
    model_test(t_path, model_path)

    """
    # 5 - 模型预测
    model_path = '../models/fasttext_model.bin'

    # print("输入待预测的语句：")
    text = '123'
    while text != 'exit':
        logger.info("输入待预测的语句：")
        sent_list = []
        sent = str(input())
        tmp = ' '.join(jieba.cut(sent))
        sent_list.append(tmp)
        # print(model_predict(sent_list, model_path))
        logger.info(model_predict(sent_list, model_path))
    """


if __name__ == '__main__':
    log_name = './logs/model_log.txt'
    logger.add(log_name, encoding='utf-8')

    model_pipeline()


    # TODO: 针对长诗句，如何整块切分。目前方法是不再加入长诗句作为用户字典的一部分
    # query = "生成与问句“小诗，山气日夕佳，飞鸟相与还。这句著名的诗句的作者你知道是谁吗？”意思必须完全相同的100条变体问句"
    #
    # sentences = { }
    # path = '../model_label/query_label/others_4.txt'
    # with open(path, 'r', encoding='utf-8') as f:
    #     for line in f.readlines():
    #         if line not in sentences:
    #             sentences[line] = 1
    #         else:
    #             sentences[line] += 1
    #
    #     f.close()
    #
    # path = '../model_label/query_label/others_5.txt'
    # with open(path, 'w', encoding='utf-8') as f:
    #     for key, _ in sentences.items():
    #         f.write(key)
    #     f.close()
    #
    # print("结束")
