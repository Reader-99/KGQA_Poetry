# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/24 11:34
 @Author: Glimmering
 @Function: #
"""
import json


# 1 - 查看数据量的大小
def dataset_size(path):
    with open(path, 'r', encoding='utf-8') as f:
        texts = json.load(f)
        print(len(texts))
        f.close()

    # max_len = 0
    # max_text = ""
    # for text in texts:
    #     tmp_len = len(text['text'])
    #     if tmp_len > max_len:
    #         max_len = tmp_len
    #         max_text = text['text']
    #
    # print("max text_len = ", max_len)
    # print(max_text)


# 2 - 对文本数据集打标签
def dataset_label():
    pass


def test():
    # 训练集与验证集的比例约为：6 : 1
    print("训练集的数据量为：")
    path = './data/example_datasets2/train_data.json'
    dataset_size(path)

    print("验证集的数据量为：")
    path = './data/example_datasets2/dev_data.json'
    dataset_size(path)
    #
    # print("测试集的数据量为：")
    # path = './data/example_datasets3/test_data.json'
    # dataset_size(path)


if __name__ == "__main__":
    test()
