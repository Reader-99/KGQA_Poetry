# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/5/2 11:11
 @Author: Glimmering
 @Function: 基于知识图谱的问答系统的相关配置
"""

import os
import json
from loguru import logger
from py2neo import Graph

# TODO: import pymysql  # 将用户的问句存储到数据库，针对其进行上下文建模

# 1 - 日志配置
log_name = './logs/' + 'robot_test' + '.txt'
logger.add(log_name, encoding='utf-8')

# 2 - neo4j 配置  # http://127.0.0.1:7474  数据传输相对较慢
graph = Graph("bolt://localhost:7687"
              , auth=("neo4j", "*******"), name='poetry')  # 用户名和密码按实际情况更改

# 3 - 实体对齐 （朝代、合称、类型、数字、姓名）
aligning_dict = {"春秋": "先秦", "战国": "先秦", "先秦": "先秦", "东汉": "两汉",  # 朝代
                 "西汉": "两汉", "两汉": "两汉", "南朝": "南北朝", "北朝": "南北朝",
                 "南北朝": "南北朝", "晋朝": "魏晋", "东晋": "魏晋", "西晋": "魏晋",
                 "晋代": "魏晋", "魏晋": "魏晋", "隋代": "隋朝", "隋朝": "隋朝",
                 "初唐": "唐代", "中唐": "唐代", "晚唐": "唐代", "唐朝": "唐代",
                 "唐代": "唐代", "五代": "五代", "南宋": "宋代", "北宋": "宋代",
                 "宋朝": "宋代", "宋代": "宋代", "金代": "金朝", "金朝": "金朝",
                 "元代": "元朝", "元朝": "元朝", "明朝": "明代", "明代": "明代",
                 "清代": "清朝", "晚清": "清朝", "清朝": "清朝", "近代": "近现代",
                 "现代": "近现代", "近现代": "近现代", "未知": "未知",
                 "高中": "高中古诗", "高中古诗": "高中古诗",                             # 作品类型
                 "四大才女": "古代四大才女"           # 作者合称
                 }

# 4 - 按照热度排序后的各朝代的作者
author_path = '/'.join(os.path.abspath(__file__).split('\\')[:-1]) + '/sorted_poems/sorted_dynasty_authors.json'
with open(author_path, 'r', encoding='utf-8') as f:
    sorted_author_of_dynasty = json.load(f)
    f.close()

# 5 - 按照热度排序后的各作者的作品
work_path = '/'.join(os.path.abspath(__file__).split('\\')[:-1]) + '/sorted_poems/sorted_author_works.json'
with open(work_path, 'r', encoding='utf-8') as f:
    sorted_work_of_author = json.load(f)
    f.close()

# 10 - 整个系统的配置
configs = {
    "logger": logger,
    "graph": graph,
    "aligning_dict": aligning_dict,
    "sorted_author_of_dynasty": sorted_author_of_dynasty,
    "sorted_work_of_author": sorted_work_of_author
}
