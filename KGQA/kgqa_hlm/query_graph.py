# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/10 13:34
 @Author: Glimmering
 @Function: 完成与红楼梦相关的问答
"""

from .spider.show_profile import get_profile  # 从当前目录导入
from .neo4j_config import graph, CA_LIST, similar_words
import codecs
import os
import json
import base64


# 1 - 界面的问答
def query(name):
    data = graph.run(
        "match(p )-[r]->(n:Person{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
            Union all\
        match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name, name)
    )
    data = list(data)
    print(data)
    return get_json_data(data)


def get_json_data(data):
    json_data = {'data': [], "links": []}
    d = []

    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name'] + "_" + i['p.cate'])
        d.append(i['n.Name'] + "_" + i['n.cate'])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")

        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
        link_item = {}

        link_item['source'] = name_dict[i['p.Name']]

        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    print(json_data)
    return json_data


# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))
def get_KGQA_answer(array):
    data_array = []
    for i in range(len(array) - 2):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['p.Name']

        data = graph.run(
            "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (
                similar_words[array[i + 1]], similar_words[array[i + 1]], name)
        )

        data = list(data)   # 输出 图谱的返回值
        print(data)
        data_array.extend(data)   # 向列表中添加另一个列表

        print("===" * 20)

    if data_array:  # 能正确回答问题
        path = '/'.join(os.path.abspath(__file__).split('\\')[:-1]) + "/spider/images/%s.jpg" % (str(data_array[-1]['p.Name']))
        with open(path, "rb") as image:
            base64_data = base64.b64encode(image.read())
            b = str(base64_data)

        return [get_json_data(data_array), get_profile(str(data_array[-1]['p.Name'])), b.split("'")[1]]
    else:
        return None


def get_answer_profile(name):
    # 获取当前路径
    path = '/'.join(os.path.abspath(__file__).split('\\')[:-1]) + '/spider/images/%s.jpg' % (str(name))
    with open(path, "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name)), b.split("'")[1]]
