# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/7 16:02
 @Author: Glimmering
 @Function: 导入所有实体节点和所有关系
"""

import sys
import json
import time

# sys.path.append(r"../data_import")
# from data_import.neo4j_config import graph

from neo4j_config import graph
from logger import Logger
from multiprocessing import Pool  # 导入进程池


class ImportNodes:
    __doc__ = "导入所有实体及部分关系"

    def __init__(self):
        self.graph = graph

    # 1 - 导入作品类型节点  对应数据库的label（WorkType：无属性）
    def import_work_type(self):
        path = '../data_nodes/node_work_type.txt'
        with open(path, 'r', encoding='utf-8') as f:
            work_types = f.readlines()
            f.close()

        for work_type in work_types:
            try:
                type = work_type.split('\n')[0]  # 作品类型
                # print(type)
                self.graph.run("MERGE( :WorkType{name: '%s'})" % type)

            except Exception as e:
                print('发生异常的作品类型：', work_type)
                print('注意异常n1：', e)
                continue

    # 2 - 导入朝代节点 对应数据库的label（Dynasty：无属性）
    def import_dynasty(self):
        path = '../data_nodes/node_dynasty.txt'
        with open(path, 'r', encoding='utf-8') as f:
            dynasties = f.readlines()
            f.close()

        for dynasty in dynasties:
            try:
                dynasty = dynasty.split('\n')[0]
                # print(dynasty)
                self.graph.run("MERGE( :Dynasty{name: '%s'})" % dynasty)
            except Exception as e:
                print('发生异常的朝代：', dynasty)
                print('注意异常n2：', e)
                continue

    # 3 - 导入合称节点（唐宋八大家） 对应数据库的label（CollectiveTitle：无属性）
    def import_collective_title(self):
        path = '../data_nodes/node_collective_title.txt'
        with open(path, 'r', encoding='utf-8') as f:
            collective_titles = f.readlines()
            f.close()

        for collective_title in collective_titles:
            try:
                collective_title = collective_title.split('\n')[0]
                # print(collective_title)
                self.graph.run("MERGE( :CollectiveTitle{name: '%s'})" % collective_title)
            except Exception as e:
                print('发生异常的合称：', collective_title)
                print('注意异常n3：', e)
                continue

    # 5 - 导入作者 对应数据库的label（Author：有属性）
    def import_author(self):
        path = '../data_nodes/node_author.json'
        with open(path, 'r', encoding='utf-8') as f:
            authors = json.load(f)
            f.close()

        # 创建性别节点 - 仅创建女，男作者居多
        self.graph.run("MERGE(: Gender{name: '%s'})" % '女')

        for author in authors:
            try:
                name = author['name']
                gender = author['gender']
                dynasty = author['dynasty']
                nationality = author['nationality']  # 民族
                origin = author['origin']  # 出生地
                date = author['date']  # 出生日期
                named = author['named']  # 李白 字太白
                b_i = author['brief_introduction']

                # 首先创建实体节点
                cypher = "MERGE( :Author{name: '%s', gender:'%s', dynasty:'%s'," \
                         " nationality: '%s',origin:'%s', date:'%s', named:'%s', brief_introduction:'%s'})"
                self.graph.run(cypher % (name, gender, dynasty, nationality, origin, date, named, b_i))

                # 然后创建对应的关系
                if gender == '女':
                    rel = "gender_is"
                    self.graph.run(
                        "MATCH (author: Author), (gender:Gender) WHERE author.name='%s' and gender.name='%s'" \
                        "MERGE (author)-[r:%s{name: '%s'}]->(gender) RETURN r"
                        % (name, '女', rel, rel)  # 关系类别为 rel, 关系名字也为 rel，无属性
                    )

                rel = "belong_to"
                self.graph.run(
                    "MATCH (author: Author), (dynasty:Dynasty) WHERE author.name='%s' and dynasty.name='%s'" \
                    "MERGE (author)-[r:%s{name: '%s'}]->(dynasty)RETURN r"
                    % (name, dynasty, rel, rel)  # 关系类别为 rel, 关系名字也为 rel，无属性
                )

            except Exception as e:
                print('发生异常的作者：', author)
                print('注意异常n5：', e)
                continue

    # 6 - 导入作者的作品数量 对应数据库的label（Author：有属性）
    def import_author_work_cnt(self):
        path = '../data_nodes/node_author_work_cnt.json'
        with open(path, 'r', encoding='utf-8') as f:
            author_work_cnt = json.load(f)
            f.close()

        for author, work_cnt in author_work_cnt.items():
            print(author)
            cypher = "match (v: Author{name: %s}) set v.work_cnt='%s' return v"
            graph.run(cypher % (author, str(work_cnt)))


class ImportRelationships:
    __doc__ = "导入部分关系"

    def __init__(self):
        self.graph = graph

    # 1 - 导入作者合称关系 对应数据库的弧（Author ->collective_title-> CollectiveTitle）
    def import_rel_collective_title(self):
        path = '../data_relationships/rel_collective_title.json'
        with open(path, 'r', encoding='utf-8') as f:
            collective_titles = json.load(f)
            f.close()

        for collective_title in collective_titles:
            try:
                author = collective_title['author']
                dynasty = collective_title['dynasty']
                title = collective_title['title']

                # 创建对应的关系
                rel = "collective_title"  # 作者写此名句
                self.graph.run(
                    "MATCH (author: Author), (c_t:CollectiveTitle) WHERE author.name='%s' "
                    "and author.dynasty='%s' and c_t.name='%s'"
                    "MERGE (author)-[r:%s{name: '%s'}]->(c_t) RETURN r"
                    % (author, dynasty, title, rel, rel)  # 可以考虑为关系添加属性
                )

            except Exception as e:
                print('发生异常的合称：', collective_title)
                print('注意异常r1：', e)
                continue

    # 2 - 导入名句类型关系 对应数据库的弧（FamousSentence ->type_is-> WorkType）
    def import_rel_fs_type(self):
        path = '../data_relationships/rel_type_of_sentence.json'
        with open(path, 'r', encoding='utf-8') as f:
            sentences = json.load(f)
            f.close()

        for sentence in sentences:
            try:
                # title = sentence['title']  可以不使用名句标题
                author = sentence['author']
                content = sentence['content']
                type = sentence['type']

                # 创建对应的关系
                rel = "type_is"  # 名句类型
                self.graph.run(
                    "MATCH (f_s: FamousSentence), (type:WorkType) "
                    "WHERE f_s.content='%s' and f_s.author='%s' and type.name='%s'"
                    "MERGE (f_s)-[r:%s{name: '%s'}]->(type) RETURN r"
                    % (content, author, type, rel, rel)  # 可以考虑为关系添加属性
                )

            except Exception as e:
                print('发生异常的名句类型：', sentence)
                print('注意异常r2：', e)
                continue

    # 3 - 导入作品类型关系 对应数据库的弧（WorkContent ->type_is-> WorkType）
    def import_rel_work_type(self):
        path = '../data_relationships/rel_type_of_work.json'
        with open(path, 'r', encoding='utf-8') as f:
            work_types = json.load(f)
            f.close()

        for work_type in work_types:
            try:
                content = work_type['content']
                type = work_type['type']

                # 创建对应的关系
                rel = "type_is"  # 作品类型
                self.graph.run(
                    "MATCH (w_c: WorkContent), (type:WorkType) "
                    "WHERE w_c.content='%s' and type.name='%s'"
                    "MERGE (w_c)-[r:%s{name: '%s'}]->(type) RETURN r"
                    % (content, type, rel, rel)  # 可以考虑为关系添加属性
                )

            except Exception as e:
                print('发生异常的作品类型：', work_type)
                print('注意异常r3：', e)
                continue


# 4 - 导入作品标题 对应数据库的label（WorkTitle：无属性）
def import_work_title(work_title):
    try:
        # print(work_title)
        graph.run("MERGE( :WorkTitle{name: '%s'})" % work_title)

    except Exception as e:
        print('发生异常的作品标题：', work_title)
        print('注意异常n4：', e)
        return


# 4 - 多进程导入作品题目
def pool_import_work_title():
    path = '../data_nodes/node_work_title.txt'
    with open(path, 'r', encoding='utf-8') as f:
        tmp_titles = f.readlines()
        f.close()

    titles = []
    for title in tmp_titles:
        title = title.split('\n')[0]
        titles.append(title)

    pool = Pool(8)  # 创建8个进程对象 print(cpu_count())
    pool.map(import_work_title, titles)


# 6 - 导入名句内容 对应数据库的label（FamousSentence：有属性）
def import_famous_sentence(famous_sentence):
    try:
        content = famous_sentence['content']  # 作品内容
        author = famous_sentence['author']
        dynasty = famous_sentence['dynasty']
        title = famous_sentence['title']  # 作品标题
        translation = famous_sentence['translation']  # 作品翻译
        annotation = famous_sentence['annotation']  # 作品注释
        appreciation = famous_sentence['appreciation']  # 作品赏析

        # 首先创建实体节点
        cypher = "MERGE( :FamousSentence{title: '%', content: '%s', author:'%s', dynasty:'%s'," \
                 " translation: '%s', annotation:'%s', appreciation:'%s'})"
        graph.run(cypher % (title, content, author, dynasty, translation, annotation, appreciation))

        # 然后创建对应的关系
        rel = "write"  # 作者写此名句
        graph.run(
            "MATCH (author: Author), (f_s:FamousSentence)"
            "WHERE author.name='%s' and f_s.content='%s'"
            "MERGE (author)-[r:%s{name: '%s'}]->(f_s) RETURN r"
            % (author, content, rel, rel)  # 可以考虑为关系添加属性
        )

        rel = "written_in"  # 名句写于某朝代
        graph.run(
            "MATCH (f_s: FamousSentence), (dynasty:Dynasty)"
            "WHERE f_s.content='%s' and dynasty.name='%s'"
            "MERGE (f_s)-[r:%s{name: '%s'}]->(dynasty) RETURN r"
            % (content, dynasty, rel, rel)  # 可以考虑为关系添加属性
        )

        rel = "title_is"  # 名句的题目
        graph.run(
            "MATCH (f_s: FamousSentence), (title: WorkTitle) "
            "WHERE f_s.content='%s' and title.name='%s'"
            "MERGE (f_s)-[r:%s{name: '%s'}]->(title) RETURN r"
            % (content, title, rel, rel)  # 可以考虑为关系添加属性
        )

    except Exception as e:
        print('发生异常的名句：', famous_sentence)
        print('注意异常n6：', e)
        return


# 6 - 多进程导入名句
def pool_import_famous_sentence():
    path = '../data_nodes/node_famous_sentence.json'
    with open(path, 'r', encoding='utf-8') as f:
        famous_sentences = json.load(f)
        f.close()

    pool = Pool(8)  # 创建8个进程对象 print(cpu_count())
    pool.map(import_famous_sentence, famous_sentences)


# 7 - 导入作品内容 对应数据库的label（WorkContent：有属性）
def import_work_content(work_content):
    try:
        title = work_content['title']  # 作品的标题
        content = work_content['content']  # 作品内容
        author = work_content['author']
        dynasty = work_content['dynasty']
        translation = work_content['translation']  # 作品翻译
        annotation = work_content['annotation']  # 作品注释
        background = work_content['background']  # 作品创作背景
        appreciation = work_content['appreciation']  # 作品赏析

        # 首先创建实体节点
        cypher = "MERGE( :WorkContent{title: '%s', content: '%s', author:'%s', dynasty:'%s'," \
                 " translation: '%s', annotation:'%s', background:'%s', appreciation:'%s'})"
        graph.run(cypher % (title, content, author, dynasty, translation, annotation, background, appreciation))

        # 然后创建对应的关系
        rel = "create"  # 作者创作作品
        graph.run(
            "MATCH (author: Author), (w_c:WorkContent)"
            "WHERE author.name='%s' and w_c.content='%s'"
            "MERGE (author)-[r:%s{name: '%s'}]->(w_c) RETURN r"
            % (author, content, rel, rel)  # 可以考虑为关系添加属性
        )

        rel = "created_in"  # 作品创作于某朝代
        graph.run(
            "MATCH (w_c: WorkContent), (dynasty:Dynasty) "
            "WHERE w_c.content='%s' and dynasty.name='%s'"
            "MERGE (w_c)-[r:%s{name: '%s'}]->(dynasty) RETURN r"
            % (content, dynasty, rel, rel)  # 可以考虑为关系添加属性
        )

        rel = "title_is"  # 作品的题目
        graph.run(
            "MATCH (w_c: WorkContent), (title: WorkTitle)"
            "WHERE w_c.content='%s' and title.name='%s'"
            "MERGE (w_c)-[r:%s{name: '%s'}]->(title) RETURN r"
            % (content, title, rel, rel)  # 可以考虑为关系添加属性
        )

        include_sentences = work_content['include']  # 加入包含的关系，直接将其写入数据库

        if not include_sentences:  # 不包含名句
            return

        rel = "include"  # 作品包含名句
        for sentence in include_sentences:
            graph.run(
                "MATCH (w_c: WorkContent), (f_s: FamousSentence) "
                "WHERE w_c.content='%s' and f_s.content='%s' and f_s.author='%s'"
                "MERGE(w_c)-[r:%s{name: '%s'}]->(f_s) RETURN r"
                % (content, sentence, author, rel, rel)  # 可以考虑为关系添加属性
            )

    except Exception as e:
        print('发生异常的作品：', work_content)
        print('注意异常n7：', e)
        return


# 7 - 多进程导入作品内容
def pool_import_work_content():
    path = '../data_nodes/node_work_content.json'
    with open(path, 'r', encoding='utf-8') as f:
        work_content = json.load(f)
        f.close()

    pool = Pool(8)  # 创建8个进程对象 print(cpu_count())
    pool.map(import_work_content, work_content)


# 8 - 导入数据控制器
def import_handler():
    # 预计导入需要 16 个小时
    print("实体导入开始……")
    i_n = ImportNodes()
    i_n.import_work_type()  # 1 - 导入作品类型
    i_n.import_dynasty()  # 2 - 导入朝代
    i_n.import_collective_title()  # 3 - 导入合称
    i_n.import_author_work_cnt()  # 导入作者的作品数量

    print("开始导入作品标题节点……")
    pool_import_work_title()  # 4 - 导入作品的标题
    time.sleep(5)
    print("作品标题节点导入结束……")

    print("开始导入作者节点……")
    i_n.import_author()  # 5 - 导入作者
    print("作者节点导入结束……")
    time.sleep(5)

    print("开始导入名句节点……")
    pool_import_famous_sentence()  # 6 - 导入名句
    print("名句节点导入结束……")
    time.sleep(5)

    print("开始导入作品节点……")
    pool_import_work_content()  # 7 - 导入作品内容，此处最耗费时间，目前没有找到更优解
    print("作品节点导入结束……")
    time.sleep(5)

    print("关系导入开始……")
    time.sleep(1)
    i_r = ImportRelationships()
    i_r.import_rel_collective_title()  # 1 - 导入作者合称关系
    i_r.import_rel_fs_type()  # 2 - 导入名句类型关系
    i_r.import_rel_work_type()  # 3 - 导入作品类型关系
    print("关系导入结束……")


# 11 - csv数据导入测试
def import_csv_data():
    # 首先创建实体节点
    cypher = """LOAD CSV WITH HEADERS FROM 'file:///node_rel_author.csv' AS row
               
     MERGE( :Author{name:row.name, gender:row.gender, dynasty:row.dynasty, nationality:row.nationality,
            origin:row.origin, date:row.date, named:row.named, brief_introduction:row.brief_introduction})
     """
    graph.run(cypher)

    """
    load csv with headers from "file:/4.csv" as line with line
 
    merge (a1:s1{name1:line.name1,pos1:line.pos1})  
     
    merge (a2:s2{name2:line.name2,pos2:line.pos2})
     
    with*match (from:s1{name1:line.name1}),(to:s2{name2:line.name2})
    merge (from)-[r:relation{relation:line.relation}]->(to)
        """
    #
    # path = 'file:///node_rel_author.csv'
    # cypher = "MERGE( :Author{name: '%s', gender:'%s', dynasty:'%s'," \
    #          " nationality: '%s',origin:'%s', date:'%s', named:'%s', brief_introduction:'%s'})"
    # self.graph.run(cypher % (name, gender, dynasty, nationality, origin, date, named, b_i))
    #
    # # 然后创建对应的关系
    # if gender == '女':
    #     rel = "gender_is"
    #     self.graph.run(
    #         "MATCH (author: Author), (gender:Gender) WHERE author.name='%s' and gender.name='%s'" \
    #         "MERGE (author)-[r:%s{name: '%s'}]->(gender) RETURN r"
    #         % (name, '女', rel, rel)  # 关系类别为 rel, 关系名字也为 rel，无属性
    #     )
    #
    # rel = "belong_to"
    # self.graph.run(
    #     "MATCH (author: Author), (dynasty:Dynasty) WHERE author.name='%s' and dynasty.name='%s'" \
    #     "MERGE (author)-[r:%s{name: '%s'}]->(dynasty)RETURN r"
    #     % (name, dynasty, rel, rel)  # 关系类别为 rel, 关系名字也为 rel，无属性
    # )
    #
    # cypher = """LOAD CSV WITH HEADERS FROM 'file:///relationship.csv' AS row
    #         MATCH (actor:actor {actorID: row.actor_Id})
    #         MATCH (movie:movie {movieID: row.movie_Id})
    #         MERGE (actor)-[:主演]->(movie)
    #         """
    # cypher = ""


if __name__ == '__main__':
    log_file_name = './log.txt'
    # 记录正常的 print 信息
    sys.stdout = Logger(log_file_name)
    # import_csv_data()  # 可将所有json文件转换成 csv 文件，然后使用neo4j 导入工具导入数据
    import_handler()





