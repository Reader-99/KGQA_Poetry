"""
 coding=utf-8
 @Software: PyCharm
 @Date: 2024/3/14 14:53
 @Author: Glimmering
 @Function: 理解用户输入的自然语言（NLU）
"""

import jieba
import fasttext as ft
from loguru import logger
from kgqa_ner.predict_ner import predict_ner
ft.FastText.eprint = lambda x: None  # 解决fasttext警告输出

# 1、用户交互模块 -> {（实体链接）属性理解：意图识别模块、属性关联} -> 推理查询模块 -> 话术包装及答案生成与返回模块
# 2、配置管理是意图理解的重要模块：通常需要对知识体系（schema）、词库（同义词词库、
# 近义词词库和分词词库、停用词词库）、问答槽位、权限等进行配置管理。
# 3、知识问答的典型的基础信息主要有实体属性词典、同义词映射词典（男生-男孩、苏轼-苏东坡等）、排序及可见信息、图结构信息和时间信息。
# 算法引擎包括模式匹配算法、语义匹配算法、时间计算算法等。
# 4、


class NaturalLanguageUnderstanding:
    __doc__ = "自然语言理解 - 理解用户输入的自然语言问句"

    def __init__(self, question, logger):
        self.question = question
        self.logger = logger
        # 都需要使用绝对路径，按需更改
        self.fasttext_model_path = r'D:\KGQA_Poetry\KGQA\models\fasttext_model.bin'
        self.bert_model_path = r'D:\KGQA_Poetry\KGQA\models\bert_ner.pth'

    # 1 - 问句意图分类
    def intent_classification(self):
        sent_list = [' '.join(jieba.cut(self.question))]  # 对分词后的问句进行分类
        cls = ft.load_model(self.fasttext_model_path)

        # 预测结果 - 二维数组
        res = cls.predict(sent_list, k=3)  # topK = 3  # 返回最可能的三种情况, threshold=0.3
        # 预测标签
        topK_labels = [label.replace('__label__', '') for label in res[0][0]]
        # 预测概率
        topK_probability = [prob for prob in res[1][0]]

        # TODO：如果第一意图概率超过0.7，且没有找到答案，那么考虑预测的第二个意图
        # print(topK_labels[0], topK_probability[0])

        # 对用户的问句解析，从而得到命名实体
        intent = topK_labels[0]  # 取候选意图的第一个
        # probability = topK_probability[0]
        entities = self.question_parse()

        logger.info("intent: " + intent)
        logger.info(entities)
        # logger.info(intents)
        print(self.question)
        return intent, entities  # 返回意图和实体，便于NLG生成答案

    # 2 - 使用 bert 模型，结合问句意图，进行问句解析（主要是命名实体识别）
    def question_parse(self):
        result = predict_ner(self.question)  # 预测问句的命名实体

        # 针对目前模型的局限性，调整输出的结果
        entities_dict = {}
        for label, entities in result.items():
            entities_dict[label] = []
            for entity in entities:
                entities_dict[label].append(entity[:-1])

        return entities_dict


if __name__ == "__main__":
    question = "我对苏轼的文学影响与其弟子们的文学贡献感兴趣，能否告诉我苏门四学士的身份？"
    nlu = NaturalLanguageUnderstanding(question, logger)
    sentence = "小诗，我对这句“举头望明月，低头思故乡”很感兴趣，它是李白的诗吗？"
    print(nlu.intent_classification())
    # print(' '.join(jieba.cut(question)))
