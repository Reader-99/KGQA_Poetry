# -*- coding: utf-8 -*-
# @Author : lishouxian
# @Email : gzlishouxian@gmail.com
# @File : config.py
# @Software: VScode

# 模式
# train:               训练分类器
# interactive_predict: 交互模式
# test:                跑测试集
# convert2tf:          将torch模型保存为onnx文件
# show_model_info:     打印模型参数
# convert2tf:将torch模型保存为tf框架的pb格式文件
# [train, interactive_predict, test, convert_onnx]
# mode = 'train'
mode = 'interactive_predict'
# mode = 'test'


# 使用CPU设备
use_cuda = False
cuda_device = 0

# 使用GPU设备
# use_cuda = True
# cuda_device = 1


configure = {
    # 训练数据集
    'train_file': 'data/example_datasets1/train_data.json',
    # 验证数据集
    'dev_file': 'data/example_datasets1/dev_data.json',
    # 没有验证集时，从训练集抽取验证集比例
    'validation_rate': 0.15,
    # 测试数据集
    'test_file': '',
    # 使用的模型
    # bp: binary pointer
    # gp: global pointer
    'model_type': 'gp',
    # 模型保存的文件夹
    'checkpoints_dir': 'checkpoints/',
    # 模型名字
    # 'model_name': 'best_model.pth',   # 对模型训练时的模型名：best_model
    'model_name': 'best_model.pth',  # 对模型训练时的模型名：best_model
    # 类别列表
    # 'classes': ['person', 'location', 'organization'],  #'WorkContent'
    'classes': ['Author', 'Dynasty', 'WorkTitle', 'Gender', 'WorkType',
                'FamousSentence', 'CollectiveTitle', 'Number'],
    # decision_threshold
    'decision_threshold': 0.5,
    # 是否使用苏神的多标签分类的损失函数，默认使用BCELoss
    'use_multilabel_categorical_cross_entropy': True,
    # 使用对抗学习
    'use_gan': False,
    # 目前支持FGM和PGD两种方法
    # fgm:Fast Gradient Method
    # pgd:Projected Gradient Descent
    'gan_method': 'pgd',
    # 对抗次数
    'attack_round': 3,
    # 是否进行warmup
    'warmup': False,
    # warmup方法，可选：linear、cosine
    'scheduler_type': 'linear',
    # warmup步数，-1自动推断为总步数的0.1
    'num_warmup_steps': -1,
    # 句子最大长度
    'max_sequence_length': 200,
    # epoch
    'epoch': 30,  # 实际训练五轮差不多达到收敛
    # batch_size
    'batch_size': 32,  # 根据 GPU 的大小更改，16、32、64 提高CPU使用效率，提高精确度
    # dropout rate
    'dropout_rate': 0.5,
    # 每print_per_batch打印损失函数
    'print_per_batch': 100,
    # learning_rate
    'learning_rate': 5e-5,
    # 优化器选择
    'optimizer': 'AdamW',
    # 训练是否提前结束微调
    'is_early_stop': True,
    # 训练阶段的patient
    'patient': 15,
}
