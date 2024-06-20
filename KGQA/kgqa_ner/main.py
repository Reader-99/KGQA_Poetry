# -*- coding: utf-8 -*-
# @Author : lishouxian
# @Email : gzlishouxian@gmail.com
# @File : main.py
# @Software: Pycharm   python = 3.9

from loguru import logger
from ner_config import use_cuda, cuda_device, configure, mode
from engines.data import DataManager
from pprint import pprint
import torch
import os
import json


def fold_check(configures):
    if configures['checkpoints_dir'] == '':
        raise Exception('checkpoints_dir did not set...')

    if not os.path.exists(configures['checkpoints_dir']):
        print('checkpoints fold not found, creating...')
        os.makedirs(configures['checkpoints_dir'])


if __name__ == '__main__':
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    fold_check(configure)
    log_name = './logs/' + mode + '.log'
    logger.add(log_name, encoding='utf-8')

    # 使用CPU 还是 GPU
    if use_cuda:
        if torch.cuda.is_available():
            if cuda_device == 1:
                device = torch.device('cuda')
            else:
                device = torch.device(f'cuda:{cuda_device}')
        else:
            raise ValueError(
                "'use_cuda' set to True when cuda is unavailable."
                " Make sure CUDA is available or set use_cuda=False."
            )
    else:
        device = 'cpu'
    logger.info(f'device: {device}')
    data_manager = DataManager(configure, logger=logger)

    if mode == 'train':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        from engines.train import Train
        logger.info('mode: train')
        Train(configure, data_manager, device, logger).train()
    elif mode == 'interactive_predict':
        print("对输入的句子进行NER预测……")
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: predict_one')
        from engines.predict import Predictor
        predictor = Predictor(configure, data_manager, device, logger)
        predictor.predict_one('warm up')
        while True:
            logger.info('please input a sentence (enter [exit] to exit.)')
            print('please input a sentence (enter [exit] to exit.)')
            sentence = input()
            if sentence == 'exit':
                break
            result = predictor.predict_one(sentence)
            pprint(result)

    elif mode == 'test':
        print("模型测试……")
        from engines.predict import Predictor
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: test')
        predictor = Predictor(configure, data_manager, device, logger)
        predictor.predict_test()

    elif mode == 'convert_onnx':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: convert_onnx')
        from engines.predict import Predictor
        predictor = Predictor(configure, data_manager, device, logger)
        predictor.convert_onnx()

    elif mode == 'show_model_info':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: show_model_info')
        from engines.predict import Predictor
        predictor = Predictor(configure, data_manager, device, logger)
        predictor.show_model_info()

# 密钥：ssh -p 35352 root@connect.bjb1.seetacloud.com