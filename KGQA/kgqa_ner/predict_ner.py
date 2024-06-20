# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/27 10:57
 @Author: Glimmering
 @Function: 进行命名实体的预测
"""

import sys
import os
import torch
import json
from pprint import pprint
from loguru import logger

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 将父文件夹加入根路径，防止导包出错
from ner_config import use_cuda, cuda_device, configure, mode
from engines.data import DataManager


# 1 - 问句命名实体识别 - 预测
def predict_ner(question):
    device = 'cpu'
    data_manager = DataManager(configure, logger=logger)

    # logger.info("对前端用户输入的问句进行 NER 预测……")
    from engines.predict import Predictor
    predictor = Predictor(configure, data_manager, device, logger)
    # predictor.predict_one('warm up')

    result = predictor.predict_one(question)  # 返回标签和实体的字典
    return result


if __name__ == '__main__':
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
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
        while True:
            logger.info('please input a sentence (enter [exit] to exit.)')
            print('please input a sentence (enter [exit] to exit.)')
            sentence = input()
            if sentence == 'exit':
                break
            result = predict_ner(sentence)
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
