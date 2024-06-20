"""
 coding=utf-8
 @Software: PyCharm
 @Date: 2024/3/14 15:02
 @Author: Glimmering
 @Function: 自然语言生成 - 生成用户需要的回答
"""
import random

# from kg_config import graph
from kgqa_config import configs


class NaturalLanguageGeneration:
    __doc__ = "自然语言生成"

    # 数字转换对应
    CN_NUM = {u'〇': 0, u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7,
              u'八': 8, u'九': 9,
              u'零': 0, u'壹': 1, u'贰': 2, u'叁': 3, u'肆': 4, u'伍': 5, u'陆': 6, u'柒': 7,
              u'捌': 8, u'玖': 9, u'貮': 2,
              u'两': 2,
              }

    CN_UNIT = {
        u'十': 10, u'拾': 10, u'百': 100, u'佰': 100, u'千': 1000, u'仟': 1000,
        u'万': 10000, u'萬': 10000, u'亿': 100000000, u'億': 100000000, u'兆': 1000000000000,
    }

    # 答案前缀
    ANSWER_PREFIX = ["聪明的小诗肯定知道啊，", "这可难不倒充满智慧的小诗，", "我可是智能小诗，",
                     "在小诗这里，这个问题一点也不难，", "嘿嘿，智能小诗，小菜一碟，", "经过我的深思熟虑，小诗了解到，",
                     "小诗感觉这个题目比较简单呢，", "这个知识小诗刚刚才学到，", "太巧啦，昨天才了解到这一知识呢,",
                     "小诗每天都在学习哦，", "这个问题的难度对于小诗来说比较适中呢，", "这个问题小诗非常感兴趣，",
                     "小诗觉得这个问题很新颖哦，", "哎呀，您的问题还有点复杂呢，",
                     "小诗刚刚在学习古诗词呢，您的问题这就回答您，",
                     "小诗可是古诗词领域的铁粉呢，马上回答您，", "古诗词领域的博才小诗，当然能够问答你的问题啦，",
                     "这个问题你找小诗就是找对啦，我可博学多才呢，", "这题我会，难不倒我智能小诗，",
                     "好累呀，小诗最近一直在学习古诗词领域的知识呢，你的这个问题可难不倒我。",
                     "经过小诗废寝忘食地学习，你的这个问题我可以回答哦，",
                     "小诗博览全书，学到了很多古诗词领域的知识呢，", "虽然你的问题比较复杂，但是小诗仍旧可以回答呢，",
                     "这个话题小诗非常感兴趣，", "还没遇见你时，小诗一直都在努力学习，你的问题我肯定能问答啦。",
                     "小诗觉得这个问题不是很难，毕竟我在古诗词领域学习很长时间了，",
                     "小诗，在古诗词领域了解了很多关于作者、作品和名句相关的知识，",
                     "小诗非常热衷于古诗词领域的各类知识呢，", "那怎么说小诗这么聪明呢，这个问题我可知道哟，",
                     "这个问题很简单哦，", "智能小诗非常开心回答你的问题，",
                     "原来你也喜欢诗词呀，小诗也很喜欢呢，我马上回答你，"]

    def __init__(self, intent, entities):  # 根据 nlu 返回的意图和实体，生成相应的答案
        self.intent = intent
        self.entities = entities
        self.graph = configs['graph']
        self.logger = configs['logger']
        self.aligning_dict = configs['aligning_dict']  # 对齐字典 - 朝代对齐、数字对齐等
        self.sorted_work_of_author = configs['sorted_work_of_author']  # 各个作者排序后的作品
        self.sorted_author_of_dynasty = configs['sorted_author_of_dynasty']  # 各个朝代的排序后的作者

    # 1 - 根据意图和命名实体，在neo4j查找，根据查找结果生成问句
    def answer_generation(self):
        answer = "太抱歉了，这个问题小诗目前还不能回答呢，我会继续学习的。但是你可以去" \
                 "咨询我的好朋友们，它们是小度、小艺、小爱同学还有Siri哦。\n"  # 兜底回答

        idx = random.randint(0, 50) % 32
        if '1' in self.intent:  # 意图类型1 - 事实型问句
            if self.intent == 'author_1':  # 询问作者相关信息 - 你知道李白哪些信息呢？介绍一下吧
                if 'Author' in self.entities:  # 是否识别出作者实体
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (v: Author{name: '%s'}) return v.dynasty, v.gender, v.work_cnt" % author
                    result = self.graph.run(cypher).data()  # 获取第一组结果
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    dynasty, gender, work_cnt = result[0].get('v.dynasty'), result[0].get('v.gender'), result[0].get(
                        'v.work_cnt')

                    if gender == '男':
                        slot = '他'
                    else:
                        slot = '她'

                    answer = "小诗目前了解到" + slot + "的情况如下所示：\n" + "姓名：" + author + "\n朝代：" \
                             + dynasty + "\n性别：" + gender + "\n作品数量：" + work_cnt

            elif self.intent == 'work_1':  # 询问某一作品 - 小诗，你好，你对行路难这首诗了解多少呢？
                if 'WorkTitle' in self.entities:  # 是否识别出标题实体
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (v: WorkContent{title: '%s'}) return v.author, v.dynasty, v.content" % title
                    results = self.graph.run(cypher).data()
                    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    work_cnt = len(results)

                    answer = "通过小诗一番思考，标题为《" + title + "》的古诗一共有 " + str(work_cnt) + " 首，分别如下所示：\n"
                    for result in results:
                        author, dynasty, content = result.get('v.author'), result.get('v.dynasty'), result.get(
                            'v.content')
                        answer += "{0:^16}".format(title) + "\n" + "{0:>8}·{1:<8}".format(author, dynasty) \
                                  + "\n" + "{0}".format(content) + '\n'

            elif self.intent == 'fs_1':  # 询问某一名句 - 你好啊，你对“人生如逆旅，我亦是行人。”这句名句了解多少呀？
                # 模型会识别出多种情况，选择最短的一种情况
                if 'FamousSentence' in self.entities:  # 是否识别出标题实体
                    tmp_fs = list(set(self.entities['FamousSentence']))
                    if len(tmp_fs) > 1:  # 包含噪音的结果，需去除
                        fs = ""
                        max_len = 100
                        for tmp in tmp_fs:
                            tmp_len = len(tmp)
                            if tmp_len < max_len:
                                max_len = tmp_len
                                fs = tmp
                    else:
                        fs = tmp_fs[0]

                    if fs[-1] != '。':  # 数据库的名句都以句号结尾
                        fs += '。'

                    cypher = "match (v: FamousSentence{content: '%s'}) return v.title, v.author, v.dynasty limit 1" % fs
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    answer = self.ANSWER_PREFIX[idx] + "这一名句的相关信息如下所示：\n"
                    title, author, dynasty = result[0].get('v.title'), result[0].get('v.author'), result[0].get(
                        'v.dynasty')
                    answer += "“" + fs + "”是" + dynasty + "的著名诗词作家" + author + "在其作品《" + title + "》中写的呢。"

            elif self.intent == 'gender_of_author_1':  # 询问作者的性别 - 你肯定知道李白的性别吧？
                if 'Author' in self.entities:  # 是否识别出作者实体
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (v: Author{name: '%s'}) return v.gender limit 1" % author
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    gender = result[0].get('v.gender')

                    if gender == '男':
                        slot = '他'
                    else:
                        slot = '她'

                    answer = self.ANSWER_PREFIX[
                                 idx] + "著名诗词作家" + author + "，" + slot + "的性别为" + gender + "性哦。"

            elif self.intent == 'dynasty_of_author_1':  # 询问作者的朝代 - 请问你知道李白是哪个朝代的吗？小诗
                if 'Author' in self.entities:  # 是否识别出作者实体
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (v: Author{name: '%s'}) return v.dynasty, v.gender limit 1" % author
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    dynasty, gender = result[0].get('v.dynasty'), result[0].get('v.gender')
                    if gender == '男':
                        slot = '他'
                    else:
                        slot = '她'

                    answer = self.ANSWER_PREFIX[
                                 idx] + "当然知道" + author + "的所属朝代啦。" + slot + "是" + dynasty + "的诗词作家呢。"

            elif self.intent == 'wc_of_author_1':  # 询问作者的作品数量 - 小诗，请问李白创作了多少作品呢？
                if 'Author' in self.entities:  # 是否识别出作者实体
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (v: Author{name: '%s'}) return v.work_cnt, v.gender limit 1" % author
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    work_cnt, gender = int(result[0].get('v.work_cnt')), result[0].get('v.gender')

                    if gender == '男':  # 槽值填充
                        slot = '他'
                    else:
                        slot = '她'
                    if work_cnt > 1000:
                        slot1 = slot + "实在是太厉害啦，根据小诗的不完全统计，"
                    else:
                        slot1 = "根据小诗的不完全统计，"

                    answer = "智多星小诗肯定了解" + author + "创作的作品数量呀。" + \
                             slot1 + slot + "一共创作了" + str(work_cnt) + "首作品呢！"

            # elif self.intent == 'nationality_of_author_1':  # 询问作者的民族、出生地、字号等，后期有时间再扩充
            #     pass

            elif self.intent == 'author_of_title_1':  # 询问某作品的作者 - 哈喽，小诗，你知不知道静夜思的作者是谁呢？
                if 'WorkTitle' in self.entities:  # 是否识别出作者实体
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答
                    cypher = "match (v: WorkContent{title: '%s'}) return v.author " % title
                    results = self.graph.run(cypher).data()
                    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    author_cnt = len(results)
                    if author_cnt > 1:
                        answer = self.ANSWER_PREFIX[idx] + "标题为《" + title + "》的诗词作品，一共有" \
                                 + str(author_cnt) + "位诗人或词人写过，" + "他们分别是："
                        for i in range(author_cnt):
                            author = results[i].get('v.author')
                            if i == author_cnt - 1:
                                answer += author + '。'
                            elif i == author_cnt - 2:
                                answer += author + '和'
                            else:
                                answer += author + '、'
                    else:
                        answer = "在小诗这里，这个问题一点也不难。标题为《" + \
                                 title + "》的诗词作品的作者是" + results[0].get('v.author') + '。'

            elif self.intent == 'dynasty_of_title_1':  # 询问某作品的朝代 - 请问静夜思是哪个朝代的古诗呀？小诗
                if 'WorkTitle' in self.entities:  # 是否识别出作者实体
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (v: WorkContent{title: '%s'}) return v.dynasty " % title
                    results = self.graph.run(cypher).data()

                    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    dynasties = []
                    for result in results:
                        for dynasty in result.values():
                            dynasties.append(dynasty)

                    author_cnt = len(results)
                    if author_cnt > 1:
                        answer = self.ANSWER_PREFIX[idx] + "标题为《" + title + "》的诗词作品，一共有" \
                                 + str(author_cnt) + "位诗人或词人写过，" + "作品分别写于："

                        for i in range(author_cnt):
                            if i == author_cnt - 1:
                                answer += dynasties[i] + '。'
                            elif i == author_cnt - 2:
                                answer += dynasties[i] + '和'
                            else:
                                answer += dynasties[i] + '、'
                    else:
                        answer = self.ANSWER_PREFIX[idx] + "标题为《" + title + "》的诗词作品写于" + results[0].get(
                            'v.dynasty') + '。'

            elif self.intent == 'content_of_title_1':  # 询问某作品的内容 - 小诗，请你告诉我静夜思的内容吧，好吗？
                if 'WorkTitle' in self.entities:  # 是否识别出作者实体
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (v: WorkContent{title: '%s'}) return v.content, v.author, v.dynasty " % title
                    results = self.graph.run(cypher).data()
                    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    contents = {}
                    for result in results:  # 存放作品的作者、朝代
                        author = result.get('v.author')
                        dynasty = result.get('v.dynasty')
                        content = result.get('v.content')
                        contents[author] = (dynasty, content)

                    author_cnt = len(results)
                    if author_cnt > 1:
                        answer = self.ANSWER_PREFIX[idx] + "标题为《" + title + "》的诗词作品，一共有 " \
                                 + str(author_cnt) + " 位诗人或词人写过，" + "内容分别为：\n"

                        cnt = 1
                        for author, content in contents.items():
                            answer += "第" + str(cnt) + "首：\n" + "{0:>8}·{1:<8}".format(content[0][:-1], author) + \
                                      '\n' + content[1] + '\n'
                            cnt += 1
                    else:
                        answer = self.ANSWER_PREFIX[idx] + "标题为《" + title + "》的作品内容为：\n" \
                                 + "{0:>8}·{1:<8}".format(results[0].get('v.dynasty')[:-1],
                                                          results[0].get('v.author')) + '\n' + results[0].get(
                            'v.content')

            # elif self.intent == 'translation_of_title_1':  # 询问某作品的翻译、写作背景、赏析等，后期有时间再扩展 - 小诗，请问静夜思这首诗如何翻译呢？
            #     pass

            elif self.intent == 'title_of_fs_1':  # 询问某名句的标题 - 小诗，请问“举头望……”来着那首诗呀？
                if 'FamousSentence' in self.entities:  # 是否识别出作者实体
                    # 模型会识别出多种情况，选择最短的一种情况
                    tmp_fs = list(set(self.entities['FamousSentence']))
                    fs = ""
                    if len(tmp_fs) > 1:  # 包含噪音的结果，需去除
                        max_len = 100
                        for tmp in tmp_fs:
                            tmp_len = len(tmp)
                            if tmp_len < max_len:
                                max_len = tmp_len
                                fs = tmp
                    else:
                        fs = tmp_fs[0]

                    if fs[-1] != '。':  # 数据库的名句都以句号结尾
                        fs += '。'

                    cypher = "match (v: FamousSentence{content: '%s'}) return v.title limit 1" % fs
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    answer = self.ANSWER_PREFIX[idx] + "该句诗“" + fs \
                             + "”" + "出自于作品《" + result[0].get('v.title') + "》。"

            elif self.intent == 'author_of_fs_1':  # 询问某名句的作者 - 你知不知道“举头望……”的作者是谁呀？小诗
                if 'FamousSentence' in self.entities:  # 是否识别出作者实体
                    # 模型会识别出多种情况，选择最短的一种情况
                    tmp_fs = list(set(self.entities['FamousSentence']))
                    fs = ""
                    if len(tmp_fs) > 1:  # 包含噪音的结果，需去除
                        max_len = 100
                        for tmp in tmp_fs:
                            tmp_len = len(tmp)
                            if tmp_len < max_len:
                                max_len = tmp_len
                                fs = tmp
                    else:
                        fs = tmp_fs[0]

                    if fs[-1] != '。':  # 数据库的名句都以句号结尾
                        fs += '。'

                    cypher = "match (v: FamousSentence{content: '%s'}) return v.author limit 1" % fs
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    answer = self.ANSWER_PREFIX[idx] + "著名诗句“" + fs \
                             + "”" + "是著名诗词作家" + result[0].get('v.author') + "所写的呢。"

            elif self.intent == 'dynasty_of_fs_1':  # 询问某名句的朝代 - 请问“人间有味是清欢。”是哪个朝代的诗人写的著名诗句呢？小诗
                if 'FamousSentence' in self.entities:  # 是否识别出作者实体
                    # 模型会识别出多种情况，选择最短的一种情况
                    tmp_fs = list(set(self.entities['FamousSentence']))
                    fs = ""
                    if len(tmp_fs) > 1:  # 包含噪音的结果，需去除
                        max_len = 100
                        for tmp in tmp_fs:
                            tmp_len = len(tmp)
                            if tmp_len < max_len:
                                max_len = tmp_len
                                fs = tmp
                    else:
                        fs = tmp_fs[0]

                    if fs[-1] != '。':  # 数据库的名句都以句号结尾
                        fs += '。'

                    cypher = "match (v: FamousSentence{content: '%s'}) return v.dynasty limit 1" % fs
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    answer = self.ANSWER_PREFIX[idx] + "目前我所知道的是，该名句“" + fs \
                             + "”" + "写于" + result[0].get('v.dynasty') + "。"

            # elif self.intent == 'translation_of_fs_1':  # 询问某名句的翻译、写作背景、赏析等，后期有时间考虑扩展 - 请问“人间有味是清欢”该如何翻译成白话文呢？小诗
            #     pass

            elif self.intent == 'work_of_author_1':  # 询问某作者的作品 - 请问苏轼写过哪些诗词呢？小诗
                if 'Author' in self.entities:  # 是否识别出作者实体
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答
                    cypher = "match (a:Author{name:'%s'}) -[r:create]->(wc:WorkContent) return" \
                             " a.work_cnt, wc.title, wc.content " % author

                    results = self.graph.run(cypher).data()
                    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    work_cnt = int(results[0]['a.work_cnt'])  # 作者的作品数量
                    if work_cnt > 1000:  # 限制呈现的数量
                        limit = 15
                    elif 1000 >= work_cnt > 10:
                        limit = 10
                    else:
                        limit = work_cnt

                    answer = self.ANSWER_PREFIX[idx] + "经小诗不完全统计，著名诗词作家" + author \
                             + "一生创作了" + str(work_cnt) + "篇作品呢。其中，著名的" \
                             + str(limit) + "篇作品如下所示：\n"

                    work_content = {}
                    for result in results:  # 获取作品标题和内容
                        title = result.get('wc.title')
                        if title not in work_content:  # TODO：存在局限，相同标题时，只能取返回的优先作品内容
                            work_content[title] = result.get('wc.content')

                    if author in self.sorted_work_of_author and limit > 10:  # 作者在排序后的字典里，并且作品数量达到10篇以上
                        cnt = 1
                        hot_works = self.sorted_work_of_author[author]  # 获取热度排序后的作品
                        for title in hot_works:
                            if title in work_content:
                                answer += "第" + str(cnt) + "篇，如下：\n" + '{0:^15}'.format(title) + '\n' + \
                                          work_content[title] + '\n'
                                cnt += 1

                            if cnt > limit:
                                break
                    else:
                        cnt = 1
                        for title, content in work_content.items():
                            answer += "第" + str(cnt) + "篇，如下：\n" + '{0:^15}'.format(title) + '\n' + work_content[
                                title] + '\n'
                            cnt += 1
                            if cnt > limit:
                                break

            elif self.intent == 'fs_of_author_1':  # 询问某作者的名句 - 小诗，我想知道李白写过的一些著名诗句，可以告诉我吗？
                if 'Author' in self.entities:  # 是否识别出作者实体
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (a:Author{name:'%s'}) -[r:write]->(f:FamousSentence)" \
                             " return count(f)" % author
                    fs_cnt = self.graph.run(cypher).data()[0].get('count(f)')  # 作者的名句数量

                    cypher = "match (a:Author{name:'%s'}) -[r:write]->(f:FamousSentence) return " \
                             "f.content, f.title" % author
                    results = self.graph.run(cypher).data()
                    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    if fs_cnt > 200:  # 限制呈现的数量
                        limit = 100
                    elif 200 >= fs_cnt > 50:
                        limit = 50
                    else:
                        limit = fs_cnt

                    answer = self.ANSWER_PREFIX[idx] + "小诗目前了解到，著名诗词作家" + author \
                             + "的名句有" + str(fs_cnt) + "句哟。其中，非常著名的" \
                             + str(limit) + "句如下所示：\n"

                    fs_content = {}
                    for result in results:  # 获取作品标题和内容
                        title = result.get('f.title')
                        if title not in fs_content:  # TODO：存在局限，相同标题时，只能取返回的优先作品内容
                            fs_content[title] = [result.get('f.content')]
                        else:
                            fs_content[title].append(result.get('f.content'))

                    if author in self.sorted_work_of_author and limit > 50:  # 作者在排序后的字典里，并且名句数量达到50句及以上
                        cnt = 1
                        hot_works = self.sorted_work_of_author[author]  # 获取热度排序后的作品
                        # print(hot_works)
                        for title in hot_works:
                            if title in fs_content:
                                for fs in fs_content[title]:
                                    answer += fs + " —— " + author + "《" + title + "》\n"
                                    cnt += 1

                            if cnt > limit:
                                break
                    else:
                        for title, content in fs_content.items():
                            for fs in content:
                                answer += fs + " —— " + author + "《" + title + "》\n"

            elif self.intent == 'author_of_dynasty_1':  # 询问某朝代的作者 - 请问唐代有哪些诗词作家呢？
                if 'Dynasty' in self.entities:  # 是否识别出作者实体
                    dynasty = list(set(self.entities['Dynasty']))[0]  # 获取问句的实体 - 取第一个实体回答

                    if dynasty in self.aligning_dict:  # 保证识别出来的朝代存在
                        dynasty = self.aligning_dict[dynasty]
                    else:
                        return answer

                    cypher = "match (d:Dynasty{name:'%s'})<-[r:belong_to]-(a:Author) return count(a)" % dynasty
                    author_cnt = self.graph.run(cypher).data()[0].get('count(a)')  # 数据库中该朝代作者的数量
                    if author_cnt > 1000:  # 控制作者显示
                        limit = 100
                    elif 1000 <= author_cnt <= 50:
                        limit = 50
                    else:
                        limit = author_cnt

                    cypher = "match (d:Dynasty{name:'%s'})<-[r:belong_to]-(a:Author) return a.name" % dynasty
                    authors = {}
                    for author in self.graph.run(cypher).data():  # 获取各朝代的作者
                        authors[author.get('a.name')] = 1

                    display_authors = []
                    for author in self.sorted_author_of_dynasty[dynasty]:  # 根据已知热度，排序输出作者
                        if author in authors:
                            display_authors.append(author)

                    author_len = len(display_authors)
                    if author_len <= limit:
                        answer = self.ANSWER_PREFIX[idx] + "经过我不完全统计，" + dynasty + \
                                 "一共有" + str(author_cnt) + "位作者呢。" + "其中非常著名的" + str(
                            author_len) + "位如下所示：\n"
                    else:
                        author_len = limit
                        answer = self.ANSWER_PREFIX[idx] + "这个问题小诗非常感兴趣，经过我不完全统计，" + dynasty + \
                                 "一共有" + str(author_cnt) + "位作者呢。" + "其中非常著名的" + str(
                            author_len) + "位如下所示：\n"

                    for i in range(author_len):  # 控制输出
                        if (i + 1) % 10 != 0 and (i + 1) != author_len:
                            answer += display_authors[i] + "、"
                        elif (i + 1) == author_len:
                            answer += display_authors[i] + "。"
                        else:
                            answer += display_authors[i] + "、\n"

            elif self.intent == 'fs_of_dynasty_1':  # 询问某朝代的名句 - 小诗，请问宋代的诗词作家写过哪些名句呢？
                if 'Dynasty' in self.entities:  # 是否识别出作者实体
                    dynasty = list(set(self.entities['Dynasty']))[0]  # 获取问句的实体 - 取第一个实体回答

                    if dynasty in self.aligning_dict:  # 保证识别出来的朝代存在
                        dynasty = self.aligning_dict[dynasty]
                    else:
                        return answer

                    cypher = "match (d:Dynasty{name:'%s'})<-[r:written_in]" \
                             "-(fs:FamousSentence) return count(fs)" % dynasty

                    fs_cnt = self.graph.run(cypher).data()[0].get('count(fs)')  # 数据库中该朝代名句的数量

                    cypher = "match (d:Dynasty{name:'%s'})<-[r:written_in]-(fs:FamousSentence)" \
                             " return fs.title, fs.author, fs.content" % dynasty
                    results = self.graph.run(cypher).data()

                    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                        return answer

                    if fs_cnt > 3000:  # 限制呈现的数量
                        limit = 200
                    elif 3000 >= fs_cnt > 100:
                        limit = 100
                    else:
                        limit = fs_cnt

                    if dynasty == "未知":  # 未知朝代，特殊处理
                        fs_content = []
                        cnt = 1
                        for result in results:  # 获取返回作者的作品标题和内容
                            if cnt > limit:
                                break
                            title = result.get('fs.title')
                            content = result.get('fs.content')
                            fs_content.append(content + " —— " + "《" + title + "》\n")
                            cnt += 1

                        answer = self.ANSWER_PREFIX[idx] + "其中小诗共收录" + dynasty \
                                 + "朝代" + str(fs_cnt) + "条名言佳句。小诗认为非常著名的 " \
                                 + str(limit) + " 句如下所示：\n"

                        for fs in fs_content:
                            answer += fs

                        return answer

                    fs_content = {}  # 按作者规整从数据库返回的名句
                    for result in results:  # 获取返回作者的作品标题和内容
                        title = result.get('fs.title')
                        author = result.get('fs.author')
                        content = result.get('fs.content')
                        if author not in fs_content:
                            fs_content[author] = [(title, content)]
                        else:
                            fs_content[author].append((title, content))

                    display_fs = []
                    for author in self.sorted_author_of_dynasty[dynasty]:  # 从知名作家开始排序输出, 如从唐代李白、白居易、杜甫开始
                        if author in fs_content:  # 作者存在于数据库中
                            cnt = 1
                            for sorted_work in self.sorted_work_of_author[author]:  # 从知名作者的知名作品开始
                                for fs in fs_content[author]:
                                    title = fs[0]
                                    content = fs[1]
                                    if title in sorted_work:  # 标题存在排序标题里
                                        display_fs.append(content + " —— " + author + "《" + title + "》\n")
                                        cnt += 1
                                        break

                                if cnt > 5:  # 每位作者只取5句
                                    break

                        if len(display_fs) > limit:
                            break

                    answer = self.ANSWER_PREFIX[idx] + "其中小诗共收录" + dynasty \
                             + "朝代" + str(fs_cnt) + "条名言佳句。小诗认为非常著名的 " \
                             + str(len(display_fs)) + " 句如下所示：\n"

                    for fs in display_fs:
                        answer += fs

            elif self.intent == 'work_of_dynasty_1':  # 询问某朝代的作品 - 小诗，可以推荐一些魏晋时期的古诗词吗？
                if 'Dynasty' in self.entities:  # 是否识别出作者实体
                    dynasty = list(set(self.entities['Dynasty']))[0]  # 获取问句的实体 - 取第一个实体回答

                    if dynasty in self.aligning_dict:  # 保证识别出来的朝代存在
                        dynasty = self.aligning_dict[dynasty]
                    else:
                        return answer

                    cypher = "match (d:Dynasty{name:'%s'})<-[r:created_in]-(wc:WorkContent) return count(wc)" % dynasty
                    wc_cnt = self.graph.run(cypher).data()[0].get('count(wc)')  # 数据库中该朝代作者的数量

                    if wc_cnt > 5000:  # 限制呈现的数量
                        limit = 100
                    elif 5000 >= wc_cnt > 1000:
                        limit = 80
                    else:
                        limit = 50

                    if dynasty == "未知":
                        cypher = "match (d:Dynasty{name:'%s'})<-[r:created_in]-(fs:WorkContent)" \
                                 " return fs.title, fs.author" % dynasty
                        results = self.graph.run(cypher).data()

                        if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                            return answer
                        work_content = []
                        cnt = 1
                        for result in results:  # 获取返回作者的作品标题和内容
                            author = result.get('fs.author')
                            title = result.get('fs.title')
                            if cnt == limit:
                                work_content.append(author + "《" + title + "》。")
                                break
                            work_content.append(author + "《" + title + "》、")
                            cnt += 1

                        answer = self.ANSWER_PREFIX[idx] + "小诗思考后知道了在小诗这里" + dynasty \
                                 + "朝代共收录了" + str(wc_cnt) + "篇作品。小诗认为非常著名的 " \
                                 + str(limit) + " 首诗词作品如下所示：\n"

                        for wc in work_content:
                            answer += wc

                        return answer

                    # 注意，由于数据库存放的作品数量达到30W以上，所以顺序返回再处理，所需时间较长，所以选择读文件输出
                    answer = self.ANSWER_PREFIX[idx] + "小诗思考后知道了在小诗这里" + dynasty \
                             + "朝代共收录了" + str(wc_cnt) + "篇作品。小诗认为非常著名的 " \
                             + str(limit) + " 首诗词作品如下所示：\n"
                    cnt = 1
                    for author in self.sorted_author_of_dynasty[dynasty]:  # 从知名作家开始排序输出, 如从唐代李白、白居易、杜甫开始
                        author_cnt = 1
                        for sorted_work in self.sorted_work_of_author[author]:  # 从知名作者的知名作品开始
                            if author_cnt > 5:  # 每位作者五篇
                                break
                            if cnt == limit:
                                answer += author + "《" + sorted_work + "》。"
                                break

                            answer += author + "《" + sorted_work + "》、"
                            cnt += 1
                            author_cnt += 1

                        if cnt == limit:  # 每位作者只取5句
                            break

            elif self.intent == 'work_of_type_1':  # 询问某类型的作品 - 你知不知道爱国类型的古诗有哪些呀？
                # TODO：由于模型识别类型的局限，以及输出的对齐，后期考虑更改
                if 'WorkType' in self.entities:  # 是否识别出作者实体
                    work_type = list(set(self.entities['WorkType']))[0]

                    cypher = "match (wt:WorkType{name:'%s'})<-[r:type_is]-(wc:WorkContent)" \
                             " return count(wc)" % work_type
                    work_cnt = self.graph.run(cypher).data()[0].get('count(wc)')  # 数据库中该类型收录的作品的数量

                    cypher = "match (wt:WorkType{name:'%s'})<-[r:type_is]-(wc:WorkContent)" \
                             " return wc.title, wc.author, wc.content, wc.dynasty" % work_type
                    results = self.graph.run(cypher).data()  # 数据库中该朝代作者的数量

                    if work_cnt == 0:
                        return answer

                    work_of_author = {}
                    for result in results:  # 规整知识图谱返回的数据
                        author = result.get('wc.author')
                        title = result.get('wc.title')
                        dynasty = result.get('wc.dynasty')
                        content = result.get('wc.content')
                        if author not in work_of_author:
                            work_of_author[author] = [(title, dynasty, content)]
                        else:
                            work_of_author[author].append((title, dynasty, content))

                    limit = 25  # 显示数量
                    answer = self.ANSWER_PREFIX[idx] + "关于" + work_type \
                             + "类型的古诗词作品小诗一共学习了" + str(work_cnt) + \
                             "篇。给您推荐其中著名的 " + str(limit) + " 篇，分别如下所示：\n"
                    cnt = 1
                    for author, works in self.sorted_work_of_author.items():
                        if author in work_of_author:
                            for work in work_of_author[author]:
                                title = work[0]
                                dynasty = work[1]
                                content = work[2]
                                if content != "暂未收录":
                                    answer += "{0:^16}".format(title) + "\n" + \
                                              "{0:>8}·{1:<8}".format(dynasty[0], author) + '\n' + content + '\n'
                                    cnt += 1

                            if cnt > limit:
                                break

            elif self.intent == 'fs_of_type_1':  # 询问某类型的名句 - 我想知道伤感风格的古代诗歌名句有哪些呢？
                # TODO：由于模型识别类型的局限，以及输出的对齐，后期考虑更改
                if 'WorkType' in self.entities:  # 是否识别出作者实体
                    fs_type = list(set(self.entities['WorkType']))[0]
                    # fs_type = self.aligning_dict[fs_type]

                    cypher = "match (wt:WorkType{name:'%s'})<-[r:type_is]-(fs:FamousSentence)" \
                             " return count(fs)" % fs_type
                    fs_cnt = self.graph.run(cypher).data()[0].get('count(fs)')  # 数据库中该类型收录的作品的数量

                    cypher = "match (wt:WorkType{name:'%s'})<-[r:type_is]-(fs:FamousSentence)" \
                             " return fs.title, fs.author, fs.content" % fs_type
                    results = self.graph.run(cypher).data()  # 该类型的所有名句

                    if fs_cnt == 0:
                        return answer

                    fs_of_author = {}
                    for result in results:  # 规整知识图谱返回的数据
                        author = result.get('fs.author')
                        title = result.get('fs.title')
                        content = result.get('fs.content')
                        if author not in fs_of_author:
                            fs_of_author[author] = [(title, content)]
                        else:
                            fs_of_author[author].append((title, content))

                    limit = 100  # 显示数量
                    cnt = 1
                    tmp_answer = " 句，它们分别是：\n"
                    for author, works in self.sorted_work_of_author.items():
                        if author in fs_of_author:
                            author_cnt = 1
                            for work in fs_of_author[author]:
                                if author_cnt > 10:  # 每个作者最多输出10条
                                    break

                                title = work[0]
                                content = work[1]
                                # 输出需加工
                                tmp_answer += content + "——" + author + "《" + title + "》" + "\n"
                                author_cnt += 1
                                cnt += 1

                        if cnt > limit:
                            break

                    answer = self.ANSWER_PREFIX[idx] + "关于" + fs_type \
                             + "类型的古诗词佳句小诗一共了解" + str(fs_cnt) + \
                             "条。给您推荐其中著名的 " + str(cnt - 1) + tmp_answer

            elif self.intent == 'type_of_work_1':  # 询问某作品的类型  - 小诗，你知不知道行路难是哪种类型的古诗呢？
                if 'WorkTitle' in self.entities:  # 是否识别出作者实体
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答

                    # 首先需要知道该标题对应了多少作品
                    cypher = "match(wc:WorkContent) -[r:title_is]-> (wt:WorkTitle{name: '%s'})" \
                             " return count(wc)" % title
                    work_cnt = self.graph.run(cypher).data()[0].get('count(wc)')  # 数据库中该朝代作者的数量

                    if work_cnt == 0:  # 表示作品不存在，或者该作品分辨不出类型来
                        return answer
                    elif work_cnt == 1:  # 该标题只对应一个作品
                        cypher = "match (wc:WorkContent{title:'%s'}) -[r:type_is]-> (wt:WorkType) " \
                                 " return wt.name " % title
                        results = self.graph.run(cypher).data()  # 该作品的类型数量

                        if not results:  # 该作品虽然在知识图谱中，但是还不知道它的类型
                            answer = "太抱歉了，小诗目前还不知道《" + title + "》这一作品的类型呢，但是我会继续学习的，争取早日知道。\n"
                            return answer

                        answer = self.ANSWER_PREFIX[idx] + "从作品《" + title + "》" + "的内容来看，小诗将其类型归类为："

                        type_cnt = len(results)
                        if type_cnt == 1:
                            answer += results[0].get('wt.name') + "类。"
                        else:
                            for i in range(type_cnt):
                                if i == type_cnt - 1:
                                    answer += "和" + results[i].get('wt.name') + "类。"
                                else:
                                    answer += results[i].get('wt.name') + "类、"

                    else:  # 改标题对应超过1个的作品，例如静夜思对应5篇作品
                        # 首先找到该标题对应的所有作品
                        cypher = "match (wc: WorkContent{title: '%s'})" \
                                 " return wc.author, wc.dynasty, wc.content" % title
                        results = self.graph.run(cypher).data()
                        title_works = {}
                        for result in results:
                            author = result.get('wc.author')
                            dynasty = result.get('wc.dynasty')
                            content = result.get('wc.content')
                            title_works[author] = (dynasty, content)

                        answer = self.ANSWER_PREFIX[idx] + "小诗目前了解到有" + str(work_cnt) \
                                 + "篇诗词作品的标题为《" + title + "》，" + "我将分别呈现给你哟。\n"

                        # 然后分别查好对应的作品，输出相关的类型
                        cnt = 1
                        for author, work in title_works.items():
                            cypher = "match (wc:WorkContent{title:'%s', author:'%s'}) -[r:type_is]-> (wt:WorkType) " \
                                     " return wt.name " % (title, author)
                            results = self.graph.run(cypher).data()  # 该作品的类型数量
                            dynasty, content = work[0], work[1]
                            answer += "第" + str(cnt) + "篇诗词作品的内容如下所示：\n"
                            answer += "{0:^16}".format(title) + "\n" + \
                                      "{0:>8}·{1:<8}".format(dynasty[0], author) + '\n' + content

                            if not results:
                                answer += "太抱歉啦，小诗目前还不知道该篇《" + title + "》的类型呢，但是我会继续学习的，争取早日知道。\n\n"
                                cnt += 1
                                continue

                            answer += "从该作品的内容来看，小诗将其类型归类为："
                            type_cnt = len(results)  # 判断作品有几种类型
                            if type_cnt == 1:
                                answer += results[0].get('wt.name') + "类。\n\n"
                            else:
                                for i in range(type_cnt):
                                    if i == type_cnt - 1:
                                        answer += "和" + results[i].get('wt.name') + "类。\n\n"
                                    else:
                                        answer += results[i].get('wt.name') + "类、"

                            cnt += 1

            elif self.intent == 'type_of_fs_1':  # 询问某名句的类型  - 小诗，我想知道“人间有味是清欢。”这句诗是哪种类型的呀？
                if 'FamousSentence' in self.entities:  # 是否识别出作者实体
                    # 模型会识别出多种情况，选择最短的一种情况
                    tmp_fs = list(set(self.entities['FamousSentence']))
                    fs = ""
                    if len(tmp_fs) > 1:  # 包含噪音的结果，需去除
                        max_len = 100
                        for tmp in tmp_fs:
                            tmp_len = len(tmp)
                            if tmp_len < max_len:
                                max_len = tmp_len
                                fs = tmp
                    else:
                        fs = tmp_fs[0]

                    if fs[-1] != '。':  # 数据库的名句都以句号结尾
                        fs += '。'

                    cypher = "match(fs:FamousSentence{content: '%s'}) -[r:type_is]-> (wt:WorkType)" \
                             " return wt.name, fs.author, fs.dynasty, fs.title" % fs
                    results = self.graph.run(cypher).data()

                    if not results:  # 找不到名句
                        answer = "非常抱歉，小诗的学识还有待提高呢。这一著名的诗句，小诗目前还不能知道它的所属类型呢。"
                        return answer

                    title = results[0].get("fs.title")
                    author = results[0].get("fs.author")
                    dynasty = results[0].get("fs.dynasty")

                    answer = self.ANSWER_PREFIX[idx] + "小诗目前了解到，著名佳句“" + fs + "”" + "是" + \
                             dynasty + "的著名诗词作家" + author + "在其作品《" + title + "》中写的。" + \
                             "从这句内容来看，小诗将其类型归类为："

                    type_cnt = len(results)
                    if type_cnt == 1:
                        answer += results[0].get('wt.name') + "类。"
                    else:
                        for i in range(type_cnt):
                            if i == type_cnt - 1:
                                answer += "和" + results[i].get('wt.name') + "类。"
                            else:
                                answer += results[i].get('wt.name') + "类、"

            elif self.intent == 'fs_of_work_1':  # 询问某作品的名句  - 请问静夜思包含哪些名句呢？
                if 'WorkTitle' in self.entities:  # 是否识别出作者实体
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答

                    # 首先查找该作品是否存在于数据库
                    cypher = "match (wc: WorkContent{title: '%s'}) return wc" % title
                    results = self.graph.run(cypher).data()
                    if not results:
                        answer = "非常抱歉，小诗的学识还有待提高呢，小诗目前没有学过作品《" + title + "》" + "。"
                        return answer

                    # 作品存在数据库中
                    cypher = "match(wc: WorkContent{title: '%s'}) -[r:include]-> (fs:FamousSentence)" \
                             " return wc.content, fs.author, fs.dynasty, fs.content" % title
                    results = self.graph.run(cypher).data()

                    if not results:  # 作品存在数据库中，但是找不到名句
                        answer = "非常抱歉，小诗的学识还有待提高呢。小诗目前还不知道作品《" + \
                                 title + "》" + "有哪些名句哟，等我继续学习之后再回答你。"
                        return answer

                    content = results[0].get("wc.content")  # 作品内容
                    author = results[0].get("fs.author")
                    dynasty = results[0].get("fs.dynasty")

                    answer = self.ANSWER_PREFIX[idx] + "它的内容如下所示：\n" + "{0:^16}".format(title) + "\n" + \
                             "{0:>8}·{1:<8}".format(dynasty[0], author) \
                             + '\n' + content + '\n' + '小诗目前了解到该作品包括如下名句：\n'

                    type_cnt = len(results)
                    if type_cnt == 1:
                        answer += "“" + results[0].get('fs.content') + "”" + '\n'
                    else:
                        for i in range(type_cnt):
                            answer += "第 " + str(i + 1) + " 句 —— " + results[i].get('fs.content') + '\n'

            elif self.intent == 'author_of_ct_1':  # 询问某合称的作者 - 你好，小诗，你是否知道唐宋八大家都是谁哦？
                if 'CollectiveTitle' in self.entities:  # 是否识别出作者实体
                    c_t = list(set(self.entities['CollectiveTitle']))[0]  # 获取问句的实体 - 取第一个实体回答

                    # 首先查找识别出来的合称是否存在于数据库
                    cypher = "match (ct: CollectiveTitle{name: '%s'}) return ct" % c_t
                    results = self.graph.run(cypher).data()

                    if not results:
                        answer = "非常抱歉，小诗的学识还有待提高，合称“" + c_t + "”目前我还不知道指的哪些诗词作家呢。"
                        return answer

                    # 作品存在数据库中
                    cypher = "match (a: Author) -[r:collective_title]-> (ct: CollectiveTitle{name: '%s'})" \
                             " return a.name, a.dynasty" % c_t
                    results = self.graph.run(cypher).data()

                    answer = self.ANSWER_PREFIX[idx] + "合称”" + c_t + "“" + "所指的是 —— "
                    rel_len = len(results)
                    for i in range(rel_len):
                        author = results[i].get('a.name')
                        dynasty = results[i].get('a.dynasty')
                        if i == rel_len - 1:
                            answer += "以及" + dynasty + "的" + author + "。"
                        elif i == rel_len - 2:
                            answer += dynasty + "的" + author
                        else:
                            answer += dynasty + "的" + author + "、"

            elif self.intent == 'author_of_female_1':  # 询问女性作者 - 小诗，请问古代的女诗人你知道是哪些吗？
                if 'Gender' in self.entities:  # 是否识别出作者实体
                    gender = list(set(self.entities['Gender']))[0]  # 获取问句的实体 - 取第一个实体回答

                    if gender == "男":
                        answer = "这个问题小诗可不可以跳过呢，因为我国古代的男性诗人、词人实在是太多啦，但是你可以让我" \
                                 "列举我国古代著名的女性诗词作家呢。"
                        return answer

                    cypher = "match (a: Author) -[r: gender_is]-> (g: Gender{name: '%s'}) " \
                             "return a.name, a.dynasty" % gender
                    results = self.graph.run(cypher).data()

                    cypher = "match (a: Author) -[r: gender_is] -> (g :Gender{name: '%s'}) return count(a)" % gender
                    author_cnt = self.graph.run(cypher).data()[0].get("count(a)")

                    answer = self.ANSWER_PREFIX[idx] + "我国古代著名的女性诗词作家" \
                                                       "一共有" + str(author_cnt) + "位，她们分别是：\n"
                    rel_len = len(results)
                    for i in range(rel_len):
                        author = results[i].get('a.name')
                        dynasty = results[i].get('a.dynasty')
                        if i % 5 == 0 and i != 0:
                            answer += "\n"
                        if i == rel_len - 1:
                            answer += "以及" + dynasty + "的" + author + "。"
                        else:
                            answer += dynasty + "的" + author + "、"

            elif self.intent == 'work_of_title_1':  # 询问某标题的作品 - 小诗，题目为静夜思的诗词有哪些呢？
                if 'WorkTitle' in self.entities:  # 是否识别出作者实体
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答

                    # 首先判断该作品是否在数据库里
                    cypher = "match (wt: WorkTitle{name: '%s'}) return wt" % title
                    result = self.graph.run(cypher).data()

                    if not result:
                        answer = "实在太抱歉啦，小诗目前还没有学过《" + title + "》" + "这篇作品呢，我会继续学习的。"
                        return answer

                    cypher = "match (wt: WorkTitle{name: '%s'}) <-[r: title_is]-" \
                             " (wc: WorkContent) return wc.author, wc.dynasty, wc.content" % title
                    results = self.graph.run(cypher).data()
                    work_cnt = len(results)

                    answer = self.ANSWER_PREFIX[idx] + "标题为《" + title \
                             + "》的作品小诗目前仅知道" + str(work_cnt) + "篇，它们分别是：\n"

                    for result in results:
                        author = result.get('wc.author')
                        dynasty = result.get('wc.dynasty')
                        content = result.get('wc.content')
                        if content == "暂未收录":
                            continue

                        answer += "{0:^16}".format(title) + "\n" + \
                                  "{0:>8}·{1:<8}".format(dynasty[0], author) \
                                  + '\n' + content + '\n'

            elif self.intent == 'type_work_dynasty_1':  # 询问在某朝代的某类型的作品 - 我想知道思乡类型的诗写于唐朝的都有哪些呀？
                if 'WorkType' in self.entities and 'Dynasty' in self.entities:  # 保证朝代和类型都是别出来了
                    work_type = list(set(self.entities['WorkType']))[0]
                    dynasty = list(set(self.entities['Dynasty']))[0]

                    if dynasty in self.aligning_dict:  # 各朝代对齐
                        dynasty = self.aligning_dict[dynasty]

                    # 首先判断该作品是否在数据库里
                    cypher = "match (wc: WorkContent{dynasty: '%s'}) -[r: type_is]-> " \
                             "(wt: WorkType{name: '%s'}) return wc.author, wc.title, wc.content" % (dynasty, work_type)
                    results = self.graph.run(cypher).data()

                    if not results:
                        answer = "不好意思，虽然小诗博览群书，但是创作于" + dynasty + "的关于" \
                                 + work_type + "类型的诗词作品，小诗目前还没有学习到呢，但是小诗会继续学习的。\n"
                        return answer

                    work_cnt = len(results)
                    if work_cnt >= 20:
                        limit = 20
                    else:
                        limit = work_cnt

                    author_works = {}
                    for result in results:  # 便于按照热度排序后输出
                        author = result.get('wc.author')
                        title = result.get('wc.title')
                        content = result.get('wc.content')
                        if content == "暂未收录":
                            continue
                        if author not in author_works:
                            author_works[author] = [(title, content)]
                        else:
                            author_works[author].append((title, content))

                    answer = self.ANSWER_PREFIX[idx] + "创作于" + dynasty + "且关于" \
                             + work_type + "类型的诗词作品，小诗目前一共了解了" \
                             + str(work_cnt) + "篇，其中非常著名的"

                    cnt = 1
                    tmp_answer = ""
                    for author in self.sorted_author_of_dynasty[dynasty]:
                        if author in author_works:
                            for title_content in author_works[author]:
                                title = title_content[0]
                                content = title_content[1]
                                tmp_answer += "{0:^16}".format(title) + "\n" + \
                                              "{0:>8}·{1:<8}".format(dynasty[0], author) \
                                              + '\n' + content + '\n'
                                cnt += 1

                        if cnt > limit:
                            break
                    answer += str(cnt) + "篇如下所示：\n" + tmp_answer

            elif self.intent == 'dynasty_author_female_1':  # 询问某朝代的女性作家 - 唐朝都有哪些女诗人呢？小诗
                if 'Dynasty' in self.entities and 'Gender' in self.entities:  # 保证朝代和性别都能够识别出来
                    dynasty = list(set(self.entities['Dynasty']))[0]
                    gender = list(set(self.entities['Gender']))[0]

                    if dynasty in self.aligning_dict:  # 保证识别出来的朝代存在
                        dynasty = self.aligning_dict[dynasty]
                    else:
                        return answer

                    if gender == "男":
                        answer = "这个问题小诗可不可以跳过呢，因为" + dynasty + "的男性诗人、词人实在是太多啦，但是你可以让我" \
                                                                               "列举该时期的女性诗词作家呢。"
                        return answer

                    cypher = "match (a:Author{gender: '%s'}) -[r:belong_to]->" \
                             " (d: Dynasty{name: '%s'}) return a.name" % (gender, dynasty)
                    results = self.graph.run(cypher).data()

                    if not results:  # 某朝代没有女作家
                        answer = "哎呀，很抱歉啦。目前，小诗还不知道" + dynasty + "有哪些著名的女性诗词作家呢。\n"
                        return answer

                    work_cnt = len(results)
                    answer = self.ANSWER_PREFIX[idx] + "目前小诗了解到，" + dynasty + "一共有" \
                             + str(work_cnt) + "位著名的女性诗词作家。她们分别是 —— "

                    if work_cnt == 1:
                        answer += results[0].get('a.name') + '。\n'
                    else:
                        for i in range(work_cnt):
                            if i == work_cnt - 1:
                                answer += "以及" + results[i].get('a.name') + '。'
                            elif i == work_cnt - 2:
                                answer += results[i].get('a.name')
                            else:
                                answer += results[i].get('a.name') + '、'

            elif self.intent == 'author_type_work_1':  # 询问某作者写过的某类型的诗 - 李白写过的思乡类型的诗都有哪些呢？你知道吗？
                if 'Author' in self.entities and 'WorkType' in self.entities:  # 保证朝代和性别都能够识别出来
                    author = list(set(self.entities['Author']))[0]
                    work_type = list(set(self.entities['WorkType']))[0]

                    # 首先判断该作者是否在数据库里
                    cypher = "match (a: Author{name: '%s'}) return a" % author
                    results = self.graph.run(cypher).data()

                    if not results:
                        answer = "非常抱歉，目前小诗还不认识" + author + "这位作家呢，但是我会去了解的。\n"
                        return answer

                    cypher = "match (wc: WorkContent{author: '%s'}) - [r: type_is] ->" \
                             " (wt: WorkType{name: '%s'}) return wc.title, wc.dynasty, wc.content" % (author, work_type)
                    results = self.graph.run(cypher).data()

                    work_cnt = len(results)
                    if work_cnt == 0:
                        answer = "虽然小诗专注于古诗词领域，但是目前并没有了解到" + author \
                                 + "是否写过哪些关于" + work_type + "类型的作品呢。"
                        return answer

                    answer = self.ANSWER_PREFIX[idx] + "著名诗词作家" + author + "一共创作了" + str(work_cnt) \
                             + "篇关于" + work_type + "类型的诗词作品，分别如下所示：\n"

                    for result in results:  # 便于按照热度排序后输出
                        dynasty = result.get('wc.dynasty')
                        title = result.get('wc.title')
                        content = result.get('wc.content')
                        if content == "暂未收录":
                            continue

                        answer += "{0:^16}".format(title) + "\n" + \
                                  "{0:>8}·{1:<8}".format(dynasty[0], author) \
                                  + '\n' + content + '\n'

            elif self.intent == 'author_type_fs_1':  # 询问某作者写过的某类型的名句 - 小诗，我想知道杜甫关于爱国写过哪些名句呢？
                if 'Author' in self.entities and 'WorkType' in self.entities:  # 保证朝代和性别都能够识别出来
                    author = list(set(self.entities['Author']))[0]
                    work_type = list(set(self.entities['WorkType']))[0]

                    # 首先判断该作者是否在数据库里
                    cypher = "match (a: Author{name: '%s'}) return a" % author
                    results = self.graph.run(cypher).data()

                    if not results:
                        answer = "非常抱歉，目前小诗还不认识" + author + "这位作家呢，但是我会去了解的。\n"
                        return answer

                    # 首先判断该作者是否在数据库里
                    cypher = "match (a: Author{name: '%s'}) return a" % author
                    results = self.graph.run(cypher).data()

                    if not results:
                        answer = "非常抱歉，目前小诗还不认识" + author + "这位作家呢，但是我会去了解的。\n"
                        return answer

                    # 匹配作者和对应类型的诗句
                    cypher = "match (fs: FamousSentence{author: '%s'}) - [r: type_is] ->" \
                             " (wt: WorkType{name: '%s'}) return fs.title, fs.dynasty, fs.content" % (author, work_type)
                    results = self.graph.run(cypher).data()

                    fs_cnt = len(results)
                    if fs_cnt == 0:
                        answer = "虽然小诗专注于古诗词领域，但是目前并没有了解到" + author \
                                 + "是否写过哪些关于" + work_type + "类型的名句呢。"
                        return answer

                    answer = self.ANSWER_PREFIX[idx] + "著名诗词作家" + author + "在其创作的作品中，一共包含了" + str(
                        fs_cnt) \
                             + "句关于" + work_type + "类型的著名佳句呢，分别如下所示：\n"

                    for result in results:  # 便于按照热度排序后输出
                        title = result.get('fs.title')
                        content = result.get('fs.content')
                        answer += content + " —— " + author + "《" + title + "》\n"

            elif self.intent == 'author_work_type_1':  # 询问某作者的某作品的类型  - 小诗，李白的静夜思这首诗是什么类型的呢？
                if 'Author' in self.entities and 'WorkTitle' in self.entities:  # 保证朝代和性别都能够识别出来
                    author = list(set(self.entities['Author']))[0]
                    title = list(set(self.entities['WorkTitle']))[0]

                    # 首先判断该作者是否在数据库里
                    cypher = "match (a: Author{name: '%s'}) return a" % author
                    results = self.graph.run(cypher).data()

                    if not results:
                        answer = "非常抱歉，目前小诗还不认识" + author + "这位作家呢，但是我会去了解的。\n"
                        return answer

                        # 判断作者是否写过某作品
                    cypher = "match (wc: WorkContent) where wc.author='%s' and wc.title='%s' " \
                             "return wc" % (author, title)
                    result = self.graph.run(cypher).data()
                    if not result:
                        answer = "哎呀，在小诗的印象里，" + author + "的所有诗词作品中好像并没有《" + \
                                 title + "》这篇作品呢。但是，你可以去问问我的好朋友们，比如小度、小艺和小爱同学。"
                        return answer

                    # 匹配作者和对应标题的作品
                    cypher = "match (wc: WorkContent{author: '%s', title: '%s'}) - [r: type_is] ->" \
                             " (wt: WorkType) return wt.name, wc.dynasty, wc.content" % (author, title)
                    results = self.graph.run(cypher).data()
                    type_cnt = len(results)

                    # 虽然作者写过这一作品，但是数据库并没有导入其类型
                    if type_cnt == 0:
                        answer = "虽然小诗专注于古诗词领域，但是目前并不知道" + author \
                                 + "的《" + title + "》属于什么类型的诗词作品呢。\n"
                        return answer

                    # 正常回答
                    answer = self.ANSWER_PREFIX[idx] + "最近刚刚了解了" + \
                             "著名诗词作家" + author + "，从其作品《" + \
                             title + "》的内容来看，小诗认为该篇作品可以归为："

                    if type_cnt == 1:
                        answer += results[0].get('wt.name') + "类。"
                    else:
                        for i in range(type_cnt):
                            if i == type_cnt - 1:
                                answer += "和" + results[i].get('wt.name') + "类。"
                            else:
                                answer += results[i].get('wt.name') + "类、"

                        # 输出作品的内容
                    answer += '\n' + "该篇作品的内容如下所示：\n"
                    dynasty = results[0].get('wc.dynasty')
                    content = results[0].get('wc.content')
                    answer += "{0:^16}".format(title) + "\n" + \
                              "{0:>8}·{1:<8}".format(dynasty[0], author) \
                              + '\n' + content + '\n'

            elif self.intent == 'author_of_wc_1':  # 询问某作品数量的作者 - 小诗，创作的作品数量超过1000的作者都有谁呢？列举一下吧
                if 'Number' in self.entities:  # 保证朝代和性别都能够识别出来
                    number = list(set(self.entities['Number']))[0]
                    work_cnt = self.digital_transformer(str(number))  # 春望

                    # 首先判断该作者是否在数据库里
                    cypher = "match (a: Author) where a.work_cnt > '%s' return a.name" % work_cnt
                    results = self.graph.run(cypher).data()

                    author_cnt = len(results)
                    if author_cnt > 20:
                        limit = 20
                    else:
                        limit = author_cnt

                    answer = self.ANSWER_PREFIX[idx] + "我所知道的作者他们的作品数量达到" + work_cnt \
                             + "的诗词作家一共有" + str(author_cnt) + "位，小诗列出" + str(limit) + "位，如下所示：\n"
                    for i in range(limit):
                        if i == limit - 1:
                            answer += "和" + results[i].get('a.name') + '。'
                        elif i == limit - 2:
                            answer += results[i].get('a.name')
                        else:
                            answer += results[i].get('a.name') + '、'

        elif '2' in self.intent:  # 意图类型2 - 是非型问句
            if self.intent == 'author_2':  # 判断某人是不是诗人、词人、作家 - 在吗，小诗，雷军是不是一个古代的诗人呢？
                if 'Author' in self.entities:
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答
                    cypher = "match (a: Author{name: '%s'}) return a.gender, a.dynasty, a.work_cnt" % author
                    result = self.graph.run(cypher).data()  # 获取第一组结果

                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        answer = "非常抱歉啦，小诗目前了解到" + author + "并不是一个诗词作家哦，" \
                                                                        "如果你不放心，可以去咨询一下我的好朋友小艺呢。\n"
                        return answer

                    dynasty, gender, work_cnt = result[0].get('a.dynasty'), result[0].get('a.gender'), result[0].get(
                        'a.work_cnt')

                    if gender == '男':
                        slot = '他'
                    else:
                        slot = '她'

                    answer = "是的，" + author + "是我国" + dynasty + "时期的著名诗词作家" + slot \
                             + "一生创作了" + str(work_cnt) + "篇的文学作品呢。\n"

            elif self.intent == 'gender_of_author_2':  # 判断某诗人的性别 - 请问李清照是不是男性词作家呀？
                if 'Author' in self.entities and 'Gender' in self.entities:
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答
                    gender = list(set(self.entities['Gender']))[0]  # 获取问句的实体 - 取第一个实体回答

                    cypher = "match (a: Author{name: '%s'}) return a.gender, a.dynasty" % author
                    result = self.graph.run(cypher).data()  # 获取第一组结果

                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        answer = "非常抱歉啦，小诗目前还不认识" + author + "，但是你可以去咨询一下我的好朋友小艺呢。\n"
                        return answer

                    neo4j_gender = result[0].get('a.gender')
                    dynasty = result[0].get('a.dynasty')
                    if neo4j_gender == "男":
                        slot = "他"
                    else:
                        slot = "她"

                    if gender == neo4j_gender:
                        answer = "没错，" + author + "是一位" + gender \
                                 + "性诗词作家呢，并且" + slot + "出生在我国" + dynasty + "时期。\n"
                    else:
                        answer = "不是的，" + author + "是一位" + neo4j_gender \
                                 + "性诗词作家呢，并且" + slot + "出生在我国" + dynasty + "时期。\n"

            elif self.intent == 'dynasty_of_author_2':  # 判断某诗人的朝代 - 李白是唐代的著名诗人吧？小诗
                if 'Author' in self.entities and 'Dynasty' in self.entities:
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答
                    dynasty = list(set(self.entities['Dynasty']))[0]  # 获取问句的实体 - 取第一个实体回答

                    if dynasty in self.aligning_dict:
                        dynasty = self.aligning_dict[dynasty]
                    else:
                        answer = "太抱歉了，目前小诗还不知道有" + dynasty + "的存在呢。\n"
                        return answer

                    cypher = "match (a: Author{name: '%s'}) return a.gender, a.dynasty, a.work_cnt" % author
                    result = self.graph.run(cypher).data()

                    if not result:  # 知识图谱中不存在该作者
                        answer = "非常抱歉啦，小诗目前还不认识" + author + "，但是你可以去咨询一下我的好朋友小艺呢。\n"
                        return answer

                    gender = result[0].get('a.gender')
                    neo4j_dynasty = result[0].get('a.dynasty')
                    work_cnt = result[0].get('a.work_cnt')
                    if gender == "男":
                        slot = "他"
                    else:
                        slot = "她"

                    if dynasty == neo4j_dynasty:
                        answer = "没错，" + author + "出生在我国的" + dynasty \
                                 + "时期，并且" + slot + "一生创作了" + str(work_cnt) + "篇文学作品呢。\n"
                    else:
                        answer = "并不是哦，" + author + "的出生朝代是" + neo4j_dynasty \
                                 + "，并且" + slot + "一生创作了" + str(work_cnt) + "篇文学作品呢。\n"

            elif self.intent == 'author_of_fs_2':  # 判断某名句的作者 - 请问名句“人间有味是清欢”是李白写的吧？小诗
                if 'Author' in self.entities and 'FamousSentence' in self.entities:
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答
                    tmp_fs = list(set(self.entities['FamousSentence']))
                    if len(tmp_fs) > 1:  # 包含噪音的结果，需去除
                        fs = ""
                        max_len = 100
                        for tmp in tmp_fs:  # 识别出来的名句，取最短的名句
                            tmp_len = len(tmp)
                            if tmp_len < max_len:
                                max_len = tmp_len
                                fs = tmp
                    else:
                        fs = tmp_fs[0]

                    if fs[-1] != '。':  # 数据库的名句都以句号结尾
                        fs += '。'

                    # 首先判断作者是否在知识图谱里
                    cypher = "match (a: Author{name: '%s'}) return a" % author
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        answer = "非常抱歉啦，小诗目前还不认识" + author + "，但是你可以去咨询一下我的好朋友小艺呢。\n"
                        return answer

                    # 然后判断坐着是否写过该名句
                    cypher = "match (a: Author{name: '%s'}) -[r: write]-> (fs: FamousSentence{content: '%s'}) " \
                             "return a.gender, fs.title, fs.dynasty " % (author, fs)
                    result = self.graph.run(cypher).data()

                    if not result:  # 不是该作者写的
                        answer = "虽然小诗才高八斗，但我并不知道" + author + "写过名句 —— “" \
                                 + fs + "“呢，你去问问我的好朋友小爱同学吧。"
                    else:
                        title = result[0].get('fs.title')
                        dynasty = result[0].get('fs.dynasty')
                        gender = result[0].get('a.gender')
                        if gender == "男":
                            slot = "他"
                        else:
                            slot = "她"

                        answer = "千真万确，小诗知道佳句“" + fs + "”是我国" + \
                                 dynasty + "著名诗词作家" + author + "写的呢，并且是" + \
                                 slot + "创作的诗词作品《" + title + "》里的一句哦。"

            elif self.intent == 'author_of_work_2':  # 判断某作品的作者 - 李白是不是写过静夜思呀？小诗
                if 'Author' in self.entities and 'WorkTitle' in self.entities:
                    author = list(set(self.entities['Author']))[0]  # 获取问句的实体 - 取第一个实体回答
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答

                    # 首先判断作者是否在知识图谱里
                    cypher = "match (a: Author{name: '%s'}) return a" % author
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        answer = "非常抱歉啦，小诗目前还不认识" + author + "，但是你可以去咨询一下我的好朋友小度呢。\n"
                        return answer

                    # 然后判断坐着是否创作了该作品
                    cypher = "match (a: Author{name: '%s'}) -[r: create]-> (wc: WorkContent{title: '%s'}) " \
                             "return a.gender, a.dynasty, wc.content " % (author, title)
                    result = self.graph.run(cypher).data()

                    if not result:  # 不是该作者的作品
                        answer = "尽管小诗常年耕耘于古诗词领域，可是我仍旧不知道" + author + "创作过《" \
                                 + title + "》呢，你去问问我的好朋友Siri吧。"
                    else:
                        content = result[0].get('wc.content')
                        dynasty = result[0].get('a.dynasty')
                        gender = result[0].get('a.gender')
                        if gender == "男":
                            slot = "他"
                        else:
                            slot = "她"

                        answer = "一点没错，小诗昨天刚学习过这篇作品呢，它的作者的确是" + author + \
                                 "。" + slot + "创作的这篇作品的内容如下所示：\n" + \
                                 "{0:^16}".format(title) + "\n" + "{0:>8}·{1:<8}".format(dynasty[0], author) \
                                 + "\n" + content + '\n'

            elif self.intent == 'type_of_work_2':  # 判断某作品的类型 - 小诗，静夜思是关于思乡的古诗吧？
                if 'WorkTitle' in self.entities and 'WorkType' in self.entities:
                    title = list(set(self.entities['WorkTitle']))[0]  # 获取问句的实体 - 取第一个实体回答
                    work_type = list(set(self.entities['WorkType']))[0]  # 获取问句的实体 - 取第一个实体回答

                    # 首先判断作品是否在知识图谱里
                    cypher = "match (wc: WorkContent{title: '%s'}) return wc" % title
                    results = self.graph.run(cypher).data()
                    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
                        answer = "十分不好意思，小诗目前还没有学习过《" + title + "》这篇作品呢，但是我会尽快去学的。\n"
                        return answer

                    # 然后判断作品的类型
                    cypher = "match (wc: WorkContent{title: '%s'}) -[r: type_is]-> (wt: WorkType) " \
                             "return wc.author, wc.dynasty, wc.content, wt.name" % title
                    results = self.graph.run(cypher).data()

                    if not results:  # 不知道该作品的类型
                        answer = "金无足赤，人无完人。小诗暂时还不知道这篇作品的类型呢，" \
                                 "但是根据其内容你可以尝试自己分类，或者寻求其它帮助哦，非常抱歉。其内容为：\n"
                        author = results[0].get('wc.author')
                        dynasty = results[0].get('wc.dynasty')
                        content = results[0].get('wc.content')
                        answer += "{0:^16}".format(title) + "\n" + "{0:>8}·{1:<8}".format(dynasty[0], author) \
                                  + "\n" + content + '\n'
                        return answer

                    # 知道该作品的类型
                    author = results[0].get('wc.author')
                    dynasty = results[0].get('wc.dynasty')
                    content = results[0].get('wc.content')

                    work_types = []  # 获取作品的所有类型
                    for result in results:
                        work_types.append(result.get('wt.name'))

                    if work_type in work_types:  # 作品和类型与 用户问句匹配
                        work_types.remove(work_type)  # 移除该类型

                        type_cnt = len(work_types)
                        if type_cnt == 1:
                            answer = "确实如你描述的这样，从《" + title + "》" + "的内容来看，小诗将其分为关于" \
                                     + work_type + "的类呢，你也可以根据它的内容，自己进行分类哟。其内容为：\n"
                        else:
                            tmp_answer = ""
                            for i in range(type_cnt):
                                if i == type_cnt - 1:
                                    tmp_answer += "和" + work_types[i] + "类。"
                                elif i == type_cnt - 2:
                                    tmp_answer += work_types[i] + "类"
                                else:
                                    tmp_answer += work_types[i] + "类、"

                            answer = "确实如你描述的这样，从《" + title + "》" + "的内容来看，小诗可以将其分为" \
                                     + work_type + "类呢，但是它也属于" + tmp_answer + "当然，你也可以根据它的内容，自己进行分类哟。其内容为：\n"

                    else:  # 类型与作品不匹配
                        answer = "不是这样的哦，小诗从《" + title + "》的内容来看，它并不属于" + work_type + \
                                 "类，而是归属于"

                        tmp_answer = ""
                        type_cnt = len(work_types)
                        for i in range(type_cnt):
                            if i == type_cnt - 1:
                                tmp_answer += "和" + work_types[i] + "类。"
                            elif i == type_cnt - 2:
                                tmp_answer += work_types[i] + "类"
                            else:
                                tmp_answer += work_types[i] + "类、"
                        answer += tmp_answer + "但同时根据其内容你可以尝试自己分类呢，其内容为：\n"

                    answer += "{0:^16}".format(title) + "\n" + "{0:>8}·{1:<8}".format(dynasty[0], author) \
                              + "\n" + content + '\n'

            elif self.intent == 'author_of_ct_2':  # 判断某合称是不是包含某作家 - 在吗？小诗，大李杜是指李白和杜甫吗？
                if 'CollectiveTitle' in self.entities and 'Author' in self.entities:
                    collective_title = list(set(self.entities['CollectiveTitle']))[0]  # 获取问句的实体 - 取第一个实体回答
                    authors = list(set(self.entities['Author']))  # 获取问句的实体 - 取第一个实体回答

                    # 首先判断合称是否在知识图谱里
                    cypher = "match (ct: CollectiveTitle{name: '%s'}) return ct" % collective_title
                    result = self.graph.run(cypher).data()
                    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
                        answer = "非常抱歉啦，虽然小诗了解过很多诗词名家的合称，但是目前还不知道合称“" \
                                 + collective_title + "“的存在呢。\n"
                        return answer

                    # 然后判断合称包含的作者
                    cypher = "match (ct: CollectiveTitle{name: '%s'}) <-[r: collective_title]-" \
                             " (a: Author) " \
                             "return a.name, a.dynasty" % collective_title
                    results = self.graph.run(cypher).data()

                    # 整合这些作者
                    neo4j_authors = {}
                    for result in results:
                        neo4j_author = result.get('a.name')
                        dynasty = result.get('a.dynasty')
                        if neo4j_author not in neo4j_authors:
                            neo4j_authors[neo4j_author] = dynasty

                    flag = True
                    for author in authors:
                        if author not in neo4j_authors:
                            flag = False

                    if flag:  # 保证都在合称里
                        tmp_answer = ""
                        author_cnt = len(authors)
                        for i in range(author_cnt):
                            if i == author_cnt - 1:
                                tmp_answer += "和" + authors[i] + "。"
                            elif i == author_cnt - 2:
                                tmp_answer += authors[i]
                            else:
                                tmp_answer += authors[i] + "、"

                        answer = "非常正确，在小诗的学习过程中，我了解到合称“" + collective_title + "”确实包括" \
                                 + tmp_answer

                        if author_cnt != len(neo4j_authors):  # 表示刚好是指这些作者
                            for author in authors:  # 去除已经输出的作者
                                neo4j_authors.pop(author)

                            answer += "而且，还包含这些诗词作家："
                            cnt = 1
                            author_cnt = len(neo4j_authors)
                            for author, dynasty in neo4j_authors.items():
                                if cnt == author_cnt:
                                    answer += "和" + dynasty + "的" + author + "。"
                                elif cnt == author_cnt - 1:
                                    answer += dynasty + "的" + author
                                else:
                                    answer += dynasty + "的" + author + "、"
                                cnt += 1

                    else:
                        tmp_answer = ""
                        author_cnt = len(authors)
                        for i in range(author_cnt):
                            if i == author_cnt - 1:
                                tmp_answer += "和" + authors[i] + "。"
                            elif i == author_cnt - 2:
                                tmp_answer += authors[i]
                            else:
                                tmp_answer += authors[i] + "、"

                        answer = "并非像你描述的那样哦，在小诗看来，" + collective_title \
                                 + "不包括" + tmp_answer + "\n而这个合称是指这些诗词作家："
                        cnt = 1
                        author_cnt = len(neo4j_authors)
                        for author, dynasty in neo4j_authors.items():
                            if cnt == author_cnt:
                                answer += "和" + dynasty + "的" + author + "。"
                            elif cnt == author_cnt - 1:
                                answer += dynasty + "的" + author
                            else:
                                answer += dynasty + "的" + author + "、"
                            cnt += 1

            # elif self.intent == 'friend_of_author_2':  # 判断作者的关系，后期有时间再扩展 - 李白和杜甫是不是朋友呢？
            #         pass

        elif '3' in self.intent:  # 意图类型3 - 对比型问句
            if self.intent == 'wc_of_author_3':  # 对比作者的作品数量 - 李白写的诗是不是比杜甫写的诗多呢？小诗
                if 'Author' in self.entities and len(self.entities['Author']) >= 2:  # 具有两个以上才有可比性
                    authors = list(set(self.entities['Author']))

                    # 首先判断两作者是否在知识图谱中
                    flag = True
                    for author in authors:
                        cypher = "match (a: Author{name: '%s'}) return a" % author
                        if not self.graph.run(cypher).data():
                            flag = False

                    if not flag:  # 不存在这些作者
                        answer = "不好意思，在小诗的学习过程中，我并没有了解过这些诗词作家，但是你可以去咨询我的好朋友天猫精灵哦。"
                        return answer

                    # 开始比较两者的情况
                    cypher = "match (a1: Author{name: '%s'}), (a2: Author{name: '%s'}) " \
                             "return a1.work_cnt > a2.work_cnt, a1.work_cnt, a2.work_cnt" % (authors[0], authors[1])

                    result = self.graph.run(cypher).data()[0]
                    judge = result.get('a1.work_cnt > a2.work_cnt')  # 布尔型

                    if judge:  # author_cnt1 > author_cnt2
                        work_cnt_1, work_cnt_2 = int(result.get('a1.work_cnt')), int(result.get('a2.work_cnt'))
                        answer = "是的没错，小诗了解到，" + authors[0] + "一生创作了" \
                                 + str(work_cnt_1) + "篇作品，而" + authors[1] \
                                 + '一生创作了' + str(work_cnt_2) + "篇作品。所以，" + \
                                 authors[0] + "的作品数量比" + authors[1] + "的作品数量多，多了" \
                                 + str(work_cnt_1 - work_cnt_2) + "篇呢。"
                    else:
                        work_cnt_1, work_cnt_2 = int(result.get('a1.work_cnt')), int(result.get('a2.work_cnt'))
                        answer = "并不是这样的，小诗了解到，" + authors[0] + "一生创作了" \
                                 + str(work_cnt_1) + "篇作品，而" + authors[1] \
                                 + '一生创作了' + str(work_cnt_2) + "篇作品。所以，" + \
                                 authors[0] + "的作品数量比" + authors[1] + "的作品数量少，少了" \
                                 + str(work_cnt_2 - work_cnt_1) + "篇呢。"

            elif self.intent == 'max_wc_3':  # 最多创作的作者 - 在吗，小诗，我想知道哪位诗人创作的作品最多呢？
                cypher = "match (a: Author) return a.work_cnt, a.dynasty, a.name, a.gender"
                results = self.graph.run(cypher).data()
                max_cnt = 5000

                author = {'max': ()}
                for result in results:
                    if not result.get('a.work_cnt'):
                        continue

                    cnt = int(result.get('a.work_cnt'))
                    if cnt > max_cnt:
                        max_cnt = cnt
                        author['max'] = (result.get('a.name'), result.get('a.gender')
                                         , result.get('a.dynasty'), max_cnt)

                if author['max'][1] == "男":
                    slot = "他"
                else:
                    slot = "她"

                answer = self.ANSWER_PREFIX[idx] + "我国古代创作最多的作者是" \
                         + author['max'][2] + "的" + author['max'][0] + "，" + slot \
                         + "一共创作了" + str(max_cnt) + "篇作品呢。"

            elif self.intent == 'dynasty_of_author_3':  # 对比作者的朝代 - 在吗？李白和苏轼出生的朝代是否相同的呢？
                if 'Author' in self.entities and len(self.entities['Author']) >= 2:  # 具有两个以上才有可比性
                    authors = list(set(self.entities['Author']))

                    # 首先判断两作者是否在知识图谱中
                    flag = True
                    for author in authors:
                        cypher = "match (a: Author{name: '%s'}) return a" % author
                        if not self.graph.run(cypher).data():
                            flag = False

                    if not flag:  # 不存在这些作者
                        answer = "不好意是，在小诗的学习过程中，我并没有了解过这些诗词作家，但是你可以去咨询我的好朋友小艺哦。"
                        return answer

                    # 开始比较两者的情况
                    cypher = "match (a1: Author{name: '%s'}), (a2: Author{name: '%s'}) " \
                             "return a1.dynasty=a2.dynasty, a1.dynasty, a2.dynasty" % (authors[0], authors[1])

                    result = self.graph.run(cypher).data()[0]
                    judge = result.get('a1.dynasty=a2.dynasty')  # 布尔型

                    if judge:  # 两作者的朝代相同
                        answer = "是的呢，小诗可以确定，" + authors[0] + "和" \
                                 + authors[1] + "都是" + result.get('a1.dynasty') + "的著名诗词作家呢。"
                    else:
                        answer = "不对哦，小诗了解到，" + authors[0] + "出生于" \
                                 + result.get('a1.dynasty') + "，而" + authors[1] + "出生在" + result.get(
                            'a2.dynasty') + "呢。"

            elif self.intent == 'cnt_of_author_3':  # 对比朝代作者的数量 - 请问唐代的诗人是不是比宋代的诗人数量多呢？
                if 'Dynasty' in self.entities and len(self.entities['Dynasty']) >= 2:  # 具有两个以上才有可比性
                    dynasties = list(set(self.entities['Dynasty']))

                    for i in range(2):  # 朝代对齐
                        if dynasties[i] not in self.aligning_dict:
                            answer = "抱歉，小诗目前还不知道朝代“" + dynasties[i] + "”的存在呢。\n"
                            return answer
                        else:
                            dynasties[i] = self.aligning_dict[dynasties[i]]

                    cypher1 = "match (a1: Author{dynasty: '%s'})  return count(a1)" % dynasties[0]
                    cypher2 = "match (a2: Author{dynasty: '%s'})  return count(a2)" % dynasties[1]
                    cnt_1 = self.graph.run(cypher1).data()[0].get('count(a1)')
                    cnt_2 = self.graph.run(cypher2).data()[0].get('count(a2)')

                    judge = cnt_1 > cnt_2
                    if judge:  # 前者大于后者
                        answer = self.ANSWER_PREFIX[idx] + "据小诗不完全统计，" + dynasties[0] + "一共有" \
                                 + str(cnt_1) + "位著名的诗词作家，而" + dynasties[1] \
                                 + "一共有" + str(cnt_2) + "位著名的诗词作家，" \
                                 + "所以前者多于后者哦。\n"
                    else:
                        answer = self.ANSWER_PREFIX[idx] + "这个问题很简单哦，据小诗不完全统计，" + dynasties[0] + "一共有" \
                                 + str(cnt_1) + "位著名的诗词作家，而" + dynasties[1] \
                                 + "一共有" + str(cnt_2) + "位著名的诗词作家，" \
                                 + "所以后者多于前者哦。\n"

        else:  # 意图类型4 - 其他与古诗词无关的对话话题，返回话术包装的结果
            answer = "闻道有先后，术业有专攻。小诗目前只专注于古诗词领域呢，其它领域的知识我还在学习中。\n" \
                     "您可以问我这样一些问题：\n" \
                     "著名诗人李白是哪个朝代的呢？\n" \
                     "小诗，你知不知道静夜思的作者是谁呢？如果知道的话请告诉我吧。\n" \
                     "在吗，我想知道《登高》这首诗的内容，你发给我吧，小诗\n" \
                     "我对苏轼的文学影响与其弟子们的文学贡献感兴趣，能否告诉我苏门四学士的身份？\n" \
                     "小诗，可以告诉我《赤壁赋》里一些经典句子吗？\n" \
                     "小诗，我想知道李白写了哪些表达思乡之情的诗，你能帮我查查吗？\n" \
                     "小诗，我被“人间有味是清欢”这句诗深深打动，这是苏轼的创作对吧？\n" \
                     "嗨呀，原来宋代有这么多诗人啊？可是你知道明代的诗人会比宋代的诗人多吗？小诗\n" \
                     "……"

        return answer

    # 2 - 中文的数字转换成阿拉伯数字
    def digital_transformer(self, cn):
        lcn = list(cn)
        unit = 0  # 当前的单位
        ldig = []  # 临时数组

        ret = 0
        tmp = 0

        if lcn[-2:] == ['零', '十']:  # “一千零十”
            ret = 10
            lcn = lcn[:-2]

        while lcn:
            cndig = lcn.pop()
            if cndig in self.CN_UNIT:  # python2: CN_UNIT.has_key(cndig)
                unit = self.CN_UNIT.get(cndig)
                if unit == 10000:
                    ldig.append('w')  # 标示万位
                    unit = 1
                elif unit == 100000000:
                    ldig.append('y')  # 标示亿位
                    unit = 1
                elif unit == 1000000000000:  # 标示兆位
                    ldig.append('z')
                    unit = 1
                continue
            else:
                dig = self.CN_NUM.get(cndig)
                if dig is None:
                    return False
                else:
                    if unit:
                        dig = dig * unit

                        if len(ldig) == 1 and isinstance(ldig[0], int) and ldig[0] < 10:  # “七百五”“七千五”的“五”不是个位
                            ldig[0] = ldig[0] * unit // 10
                        if len(ldig) == 2 and isinstance(ldig[0], int) and ldig[0] < 10:  # “七亿五”“七万五”的“五”不是个位
                            if ldig[-1] == 'w':
                                ldig[0] = ldig[0] * 1000
                            elif ldig[-1] == 'y':
                                ldig[0] = ldig[0] * 10000000
                            elif ldig[-1] == 'z':
                                ldig[0] = ldig[0] * 100000000000
                        unit = 0

                    ldig.append(dig)

        if unit == 10:  # 处理10-19的数字
            ldig.append(10)

        while ldig:
            x = ldig.pop()
            if x == 'w':
                tmp *= 10000
                ret += tmp
                tmp = 0
            elif x == 'y':
                tmp *= 100000000
                ret += tmp
                tmp = 0
            elif x == 'z':
                tmp *= 1000000000000
                ret += tmp
                tmp = 0
            else:
                tmp += x
        ret += tmp
        return str(ret)
