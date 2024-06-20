# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/3/1 11:09
 @Author: Glimmering
 @Function: 创建红楼梦知识图谱
"""

from logger import Logger
from neo4j_config import graph
import sys


# 导入 红楼梦 的所有节点和关系
def import_hlm_data():
    path = '../KGQA/kgqa_hlm/spider/json/hlm_relation.txt'
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            rela_array = line.strip("\n").split(",")
            print(rela_array)
            graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (rela_array[3], rela_array[0]))
            graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
            graph.run(
                "MATCH(e: Person), (cc: Person) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[1], rela_array[2], rela_array[2])
            )
        f.close()


if __name__ == '__main__':
    log_file_name = './log.txt'
    # 记录正常的 print 信息
    sys.stdout = Logger(log_file_name)
    import_hlm_data()
