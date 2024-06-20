# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/5/15 16:57
 @Author: Glimmering
 @Function: 前端图谱查询作者和作品
"""

from kgqa_config import graph, sorted_work_of_author

category = {"Author": 0, "CollectiveTitle": 1, "Dynasty": 2, "FamousSentence": 3, "Gender": 4, "WorkContent": 5,
            "WorkTitle": 6, "WorkType": 7}


# 1 - 界面有关作品和作者的问答
def query_author_work(author_work):
    cypher = "match (a: Author{name: '%s'}) return a.gender" % author_work
    if graph.run(cypher).data():  # 询问的是作者
        a = 10
    else:  # 询问的是作品
        a = 10

    # 显示作者
    author = author_work
    json_data = {'data': [], "links": []}
    # 获取作者的性别和朝代
    cypher = "match(a: Author{name:'%s'}) return a.dynasty, a.gender" % author
    result = graph.run(cypher).data()[0]

    name_index = {}
    index = 0
    json_data['data'].append({'name': author, 'category': category['Author']})
    name_index[author] = index

    # 朝代
    index += 1
    dynasty = result.get('a.dynasty')
    json_data['data'].append({'name': dynasty, 'category': category['Dynasty']})
    name_index[dynasty] = index
    json_data['links'].append({'source': name_index[author], 'target': name_index[dynasty], 'value': 'belong_to'})

    # 性别
    index += 1
    gender = result.get('a.gender')
    json_data['data'].append({'name': gender, 'category': category['Gender']})
    name_index[gender] = index
    json_data['links'].append({'source': name_index[author], 'target': name_index[gender], 'value': 'gender_is'})

    # 作品
    cypher = "match(wc: WorkContent{author:'%s'}) return wc.title" % author
    results = graph.run(cypher).data()

    work_content = {}
    for result in results:  # 获取作品标题
        title = result.get('wc.title')
        if title not in work_content:
            work_content[title] = title

    if author in sorted_work_of_author:  # 作者在排序后的字典里，并且作品数量达到10篇以上
        cnt = 1
        hot_works = sorted_work_of_author[author]  # 获取热度排序后的作品
        for title in hot_works:
            if title in work_content:
                index += 1
                json_data['data'].append({'name': title, 'category': category['WorkTitle']})
                name_index[title] = index
                json_data['links'].append(
                    {'source': name_index[author], 'target': name_index[title], 'value': 'create'})
                cnt += 1
                if cnt > 5:  # 仅展现5个著名作品
                    break

    # 名句
    cypher = "match (a:Author{name:'%s'}) -[r:write]->(f:FamousSentence) return " \
             "f.content, f.title" % author
    results = graph.run(cypher).data()

    fs_content = {}
    for result in results:  # 获取作品标题和内容
        title = result.get('f.title')
        if title not in fs_content:
            fs_content[title] = [result.get('f.content')]
        else:
            fs_content[title].append(result.get('f.content'))

    if author in sorted_work_of_author:  # 作者在排序后的字典里，并且名句数量达到50句及以上
        cnt = 1
        hot_works = sorted_work_of_author[author]  # 获取热度排序后的作品
        for title in hot_works:
            if title in fs_content:
                for fs in fs_content[title]:
                    index += 1
                    json_data['data'].append({'name': fs, 'category': category['FamousSentence']})
                    name_index[fs] = index
                    json_data['links'].append(
                        {'source': name_index[author], 'target': name_index[fs], 'value': 'write'})
                    cnt += 1
                    if cnt > 5:
                        break
            if cnt > 5:
                break

    return json_data
