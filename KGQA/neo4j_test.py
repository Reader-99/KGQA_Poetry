# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/5/2 10:53
 @Author: Glimmering
 @Function: neo4j 测试
"""
from py2neo import Graph
from kgqa_config import sorted_author_of_dynasty, sorted_work_of_author, aligning_dict


def query(graph):
    answer = "太抱歉了，这个问题小诗目前还不能回答呢，但是我会继续学习的。\n"
    # 1 - author_1
    """
    author = "李白"
    cypher = "match (v: Author{name: '%s'}) return v.dynasty, v.gender, v.work_cnt" % author

    results = graph.run(cypher).data()[0]
    dynasty, gender, work_cnt = results.get('v.dynasty'), results.get('v.gender'), results.get('v.work_cnt')
    print(dynasty, gender, work_cnt)
    if gender == '男':
        slot = '他'
    else:
        slot = '她'

   answer = "小诗目前了解到" + slot + "的情况如下所示：\n" + "姓名：" + author + "\n朝代：" \
          + dynasty + "\n性别：" + gender + "\n作品数量：" + work_cnt

    """

    # 2 - work_1
    """
    title = '静夜思'
    cypher = "match (v: WorkContent{title: '%s'}) return v.author, v.dynasty, v.content" % title
    results = graph.run(cypher).data()
    work_cnt = len(results)

    answer = "通过小诗一番思考，标题为《" + title + "》的古诗一共有 " + str(work_cnt) + " 首，分别如下所示：\n"
    for result in results:
        author, dynasty, content = result.get('v.author'), result.get('v.dynasty'), result.get('v.content')
        answer += "{0:^16}".format(title) + "\n" + "{0:>8}·{1:<8}".format(author, dynasty) \
                  + "\n" + "{0}".format(content) + '\n'
    print(answer)"""

    # 3 - fs_1
    """
    fs = "人生如逆旅，我亦是行人。"
    cypher = "match (v: FamousSentence{content: '%s'}) return v.title, v.author, v.dynasty limit 1" % fs
    result = graph.run(cypher).data()[0]
    print(result)

    answer = "聪明的小诗肯定知道啊，这一名句的相关信息如下所示：\n"
    title, author, dynasty = result.get('v.title'), result.get('v.author'), result.get('v.dynasty')
    answer += "“" + fs + "”是" + dynasty + "的著名诗词作家" + author + "在其作品《" + title + "》写的呢。"
    print(answer)"""

    # 4 - gender_of_author_1
    """
    author = "王安石"
    cypher = "match (v: Author{name: '%s'}) return v.gender limit 1" % author
    result = graph.run(cypher).data()[0]
    print(result)
    gender = result.get('v.gender')
    if gender == '男':
        slot = '他'
    else:
        slot = '她'

    answer = "这可难不倒充满智慧的小诗，著名诗词作家" + author + "，" + slot + "的性别为" + gender + "性哦。"
    print(answer)"""

    # 5 - dynasty_of_author_1
    """
    author = "李清照"
    cypher = "match (v: Author{name: '%s'}) return v.dynasty, v.gender limit 1" % author
    result = graph.run(cypher).data()[0]
    print(result)
    dynasty, gender = result.get('v.dynasty'), result.get('v.gender')
    if gender == '男':
        slot = '他'
    else:
        slot = '她'

    answer = "我可是智能小诗，当然知道" + author + "的所属朝代啦。" + slot + "是" + dynasty + "的诗词作家呢。"
    print(answer)
    """

    # 6 - wc_of_author_1
    """
    author = "陆游"
    cypher = "match (v: Author{name: '%s'}) return v.work_cnt, v.gender limit 1" % author
    result = graph.run(cypher).data()[0]
    print(result)
    work_cnt, gender = int(result.get('v.work_cnt')), result.get('v.gender')
    if gender == '男':
        slot = '他'
    else:
        slot = '她'
    if work_cnt > 1000:
        slot1 = slot + "实在是太厉害啦，根据小诗的不完全统计，"
    else:
        slot1 = "根据小诗的不完全统计，"
    answer = "智多星小诗肯定了解" + author + "创作的作品数量呀。" + \
             slot1 + slot + "一共创作了" + str(work_cnt) + "首作品呢！"
    print(answer)"""

    # 7 - author_of_title_1
    """
    answer = "太抱歉了，这个问题小诗目前还不能回答呢，但是我会继续学习的。\n"
    title = "楚女谣"
    cypher = "match (v: WorkContent{title: '%s'}) return v.author " % title
    results = graph.run(cypher).data()
    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    print(results)
    author_cnt = len(results)
    if author_cnt > 1:
        answer = "在小诗这里，这个问题一点也不难。标题为《" + title + "》的诗词作品，一共有" \
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
        author = results[0].get('v.author')
        answer = "在小诗这里，这个问题一点也不难。标题为《" + title + "》的诗词作品的作者是" + author + '。'
    """

    # 8 - dynasty_of_title_1
    """
    title = "静夜思"
    cypher = "match (v: WorkContent{title: '%s'}) return v.dynasty " % title
    results = graph.run(cypher).data()
    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    print(results)
    dynasties = []
    for result in results:
        for dynasty in result.values():
            dynasties.append(dynasty)

    author_cnt = len(results)
    if author_cnt > 1:
        answer = "嘿嘿，智能小诗，小菜一碟。标题为《" + title + "》的诗词作品，一共有" \
                 + str(author_cnt) + "位诗人或词人写过，" + "作品分别写于："

        for i in range(author_cnt):
            if i == author_cnt - 1:
                answer += dynasties[i] + '。'
            elif i == author_cnt - 2:
                answer += dynasties[i] + '和'
            else:
                answer += dynasties[i] + '、'
    else:
        answer = "在小诗这里，这个问题一点也不难。标题为《" + title + "》的诗词作品写于" + results[0].get('v.dynasty') + '。'
    """

    # 9 - content_of_title_1
    """
    title = "定风波·莫听穿林打叶声"
    cypher = "match (v: WorkContent{title: '%s'}) return v.content " % title
    results = graph.run(cypher).data()
    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    print(results)
    content = []
    for result in results:
        for value in result.values():
            content.append(value)

    author_cnt = len(results)
    if author_cnt > 1:
        answer = "经过我的深思熟虑，小诗了解到，标题为《" + title + "》的诗词作品，一共有" \
                 + str(author_cnt) + "位诗人或词人写过，" + "内容分别为：\n"

        for i in range(author_cnt):
            answer += "第" + str(i + 1) + "首：\n" + content[i] + '\n'

    else:
        answer = "经过我的深思熟虑，小诗了解到，标题为《" + title + "》的作品内容为：\n" + results[0].get('v.content')
    """

    # 10 - title_of_fs_1
    """
    fs = "问君能有几多愁？恰似一江春水向东流。"
    cypher = "match (v: FamousSentence{content: '%s'}) return v.title limit 1" % fs
    result = graph.run(cypher).data()
    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    print(result)
    answer = "小诗感觉这个题目比较简单呢，该句诗“" + fs\
             + "”" + "出自于作品《" + result[0].get('v.title') + "》。"
             """

    # 11 - author_of_fs_1
    """
    fs = "东临碣石，以观沧海。"
    cypher = "match (v: FamousSentence{content: '%s'}) return v.author limit 1" % fs
    result = graph.run(cypher).data()
    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    print(result)
    answer = "这个知识小诗刚刚才学到，著名诗句“" + fs \
             + "”" + "是著名诗词作家" + result[0].get('v.author') + "所写的呢。"
    print(answer)"""

    # 12 - dynasty_of_fs_1
    """
    fs = "朱桂黝倏于南北，兰芝阿那于东西。"
    cypher = "match (v: FamousSentence{content: '%s'}) return v.dynasty limit 1" % fs
    result = graph.run(cypher).data()
    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    print(result)
    answer = "太巧啦，昨天才了解到这一知识呢。目前我所知道的是，该名句“" + fs \
             + "”" + "写于" + result[0].get('v.dynasty') + "。"
    print(answer)"""

    # 13 - work_of_author_1
    """
    author = "王安石"
    cypher = "match (a:Author{name:'%s'}) -[r:create]->(w:WorkContent) return" \
             " a.work_cnt, w.title, w.content " % author
    results = graph.run(cypher).data()
    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    work_cnt = int(results[0]['a.work_cnt'])  # 作者的作品数量
    if work_cnt > 1000:  # 限制呈现的数量
        limit = 15
    elif 1000 >= work_cnt > 10:
        limit = 10
    else:
        limit = work_cnt

    answer = "小诗每天都在学习哦，经小诗不完全统计，著名诗词作家" + author \
             + "一生创作了" + str(work_cnt) + "篇作品呢。其中，著名的" \
             + str(limit) + "篇作品如下所示：\n"

    work_content = {}
    for result in results:  # 获取作品标题和内容
        title = result.get('w.title')
        if title not in work_content:  # TODO：存在局限，相同标题时，只能取返回的优先作品内容
            work_content[title] = result.get('w.content')

    if author in sorted_work_of_author and limit > 10:  # 作者在排序后的字典里，并且作品数量达到10篇以上
        cnt = 1
        hot_works = sorted_work_of_author[author]  # 获取热度排序后的作品
        # print(hot_works)
        for title in hot_works:
            if title in work_content:
                # print(title)
                answer += "第" + str(cnt) + "篇，如下：\n" + '{0:^15}'.format(title) + '\n' + work_content[title] + '\n'
                cnt += 1

            if cnt > limit:
                break
    else:
        cnt = 1
        for title, content in work_content.items():
            answer += "第" + str(cnt) + "篇，如下：\n" + '{0:^15}'.format(title) + '\n' + work_content[title] + '\n'
            cnt += 1
            if cnt > limit:
                break
    """

    # 14 - fs_of_author_1
    """
    author = "颜真卿"
    cypher = "match (a:Author{name:'%s'}) -[r:write]->(f:FamousSentence)" \
             " return count(f)" % author
    fs_cnt = graph.run(cypher).data()[0].get('count(f)')  # 作者的名句数量

    cypher = "match (a:Author{name:'%s'}) -[r:write]->(f:FamousSentence) return " \
             "f.content, f.title" % author
    results = graph.run(cypher).data()

    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    if fs_cnt > 200:  # 限制呈现的数量
        limit = 100
    elif 200 >= fs_cnt > 50:
        limit = 50
    else:
        limit = fs_cnt

    answer = "这个问题的难度对于小诗来说比较适中呢，小诗目前了解到，著名诗词作家" + author \
             + "的名句有" + str(fs_cnt) + "句哟。其中，非常著名的 " \
             + str(limit) + " 句如下所示：\n"

    fs_content = {}
    for result in results:  # 获取作品标题和内容
        title = result.get('f.title')
        if title not in fs_content:  # TODO：存在局限，相同标题时，只能取返回的优先作品内容
            fs_content[title] = [result.get('f.content')]
        else:
            fs_content[title].append(result.get('f.content'))

    if author in sorted_work_of_author and limit > 50:  # 作者在排序后的字典里，并且名句数量达到50句及以上
        cnt = 1
        hot_works = sorted_work_of_author[author]  # 获取热度排序后的作品
        # print(hot_works)
        for title in hot_works:
            if title in fs_content:
                for fs in fs_content[title]:
                    answer += fs + " ———— " + author + "《" + title + "》\n"
                    cnt += 1

            if cnt > limit:
                break
    else:
        for title, content in fs_content.items():
            for fs in content:
                answer += fs + " ———— " + author + "《" + title + "》\n"
    """

    # 15 - author_of_dynasty_1
    """
    dynasty = "宋代"
    if dynasty in aligning_dict:  # 保证识别出来的朝代存在
        dynasty = aligning_dict[dynasty]
    else:
        return answer
    cypher = "match (d:Dynasty{name:'%s'})<-[r:belong_to]-(a:Author) return count(a)" % dynasty

    author_cnt = graph.run(cypher).data()[0].get('count(a)')  # 数据库中该朝代作者的数量

    if author_cnt > 1000:  # 控制作者显示
        limit = 100
    elif 1000 <= author_cnt <= 50:
        limit = 50
    else:
        limit = author_cnt

    cypher = "match (d:Dynasty{name:'%s'})<-[r:belong_to]-(a:Author) return a.name" % dynasty
    authors = {}
    for author in graph.run(cypher).data():  # 获取各朝代的作者
        authors[author.get('a.name')] = 1

    display_authors = []
    for author in sorted_author_of_dynasty[dynasty]:  # 根据已知热度，排序输出作者
        if author in authors:
            display_authors.append(author)

    author_len = len(display_authors)
    if author_len <= limit:
        answer = "这个问题小诗非常感兴趣，经过我不完全统计，" + dynasty + \
                "一共有" + str(author_cnt) + "位作者呢。" + "其中非常著名的" + str(author_len) + "位如下所示：\n"
    else:
        author_len = limit
        answer = "这个问题小诗非常感兴趣，经过我不完全统计，" + dynasty + \
                 "一共有" + str(author_cnt) + "位作者呢。" + "其中非常著名的" + str(author_len) + "位如下所示：\n"

    for i in range(author_len):  # 控制输出
        if (i + 1) % 10 != 0 and (i + 1) != author_len:
            answer += display_authors[i] + "、"
        elif (i + 1) == author_len:
            answer += display_authors[i] + "。"
        else:
            answer += display_authors[i] + "、\n"

    print(answer)
    """

    # 16 - fs_of_dynasty_1
    """
    dynasty = "唐朝"
    if dynasty in aligning_dict:  # 保证识别出来的朝代存在
        dynasty = aligning_dict[dynasty]
    else:
        return answer
    cypher = "match (d:Dynasty{name:'%s'})<-[r:written_in]-(fs:FamousSentence) return count(fs)" % dynasty
    # cypher = "match (d:Dynasty{name:'%s'})<-[r:created_in]-(wc:WorkContent) return count(wc)" % dynasty

    fs_cnt = graph.run(cypher).data()[0].get('count(fs)')  # 数据库中该朝代作者的数量

    cypher = "match (d:Dynasty{name:'%s'})<-[r:written_in]-(fs:FamousSentence)" \
             " return fs.title, fs.author, fs.content" % dynasty
    results = graph.run(cypher).data()

    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
        return answer

    if fs_cnt > 3000:  # 限制呈现的数量
        limit = 200
    elif 3000 >= fs_cnt > 100:
        limit = 100
    else:
        limit = fs_cnt

    if dynasty == "未知":
        fs_content = []
        cnt = 1
        for result in results:  # 获取返回作者的作品标题和内容
            if cnt > limit:
                break
            title = result.get('fs.title')
            content = result.get('fs.content')
            fs_content.append(content + " ———— " + "《" + title + "》\n")
            cnt += 1

        answer = "小诗觉得这个问题很新颖哦，其中小诗共收录" + dynasty \
                 + "朝代" + str(fs_cnt) + "条名言佳句。小诗认为非常著名的 " \
                 + str(limit) + " 句如下所示：\n"

        for fs in fs_content:
            answer += fs

        print(answer)
        return answer

    fs_content = {}
    for result in results:  # 获取返回作者的作品标题和内容
        title = result.get('fs.title')
        author = result.get('fs.author')
        content = result.get('fs.content')
        if author not in fs_content:
            fs_content[author] = [(title, content)]
        else:
            fs_content[author].append((title, content))

    display_fs = []
    for author in sorted_author_of_dynasty[dynasty]:  # 从知名作家开始排序输出, 如从唐代李白、白居易、杜甫开始
        if author in fs_content:  # 作者存在于数据库中
            cnt = 1
            for sorted_work in sorted_work_of_author[author]:  # 从知名作者的知名作品开始
                for fs in fs_content[author]:
                    title = fs[0]
                    content = fs[1]
                    if title in sorted_work:  # 标题存在排序标题里
                        display_fs.append(content + " ———— " + author + "《" + title + "》\n")
                        cnt += 1
                        break

                if cnt > 5:  # 每位作者只取5句
                    break

        if len(display_fs) > limit:
            break

    answer = "小诗觉得这个问题很新颖哦，其中小诗共收录" + dynasty \
             + "朝代" + str(fs_cnt) + "条名言佳句。小诗认为非常著名的 " \
             + str(len(display_fs)) + " 句如下所示：\n"

    for fs in display_fs:
        answer += fs

    print(answer)"""

    # 17 - work_of_dynasty_1
    """
    dynasty = "宋代"
    if dynasty in aligning_dict:  # 保证识别出来的朝代存在
        dynasty = aligning_dict[dynasty]
    else:
        return answer
    cypher = "match (d:Dynasty{name:'%s'})<-[r:created_in]-(wc:WorkContent) return count(wc)" % dynasty

    wc_cnt = graph.run(cypher).data()[0].get('count(wc)')  # 数据库中该朝代作者的数量

    if wc_cnt > 5000:  # 限制呈现的数量
        limit = 150
    elif 5000 >= wc_cnt > 1000:
        limit = 100
    else:
        limit = 50

    if dynasty == "未知":
        cypher = "match (d:Dynasty{name:'%s'})<-[r:created_in]-(fs:WorkContent)" \
                 " return fs.title, fs.author" % dynasty
        results = graph.run(cypher).data()

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

        answer = "哎呀，您的问题还有点复杂呢，小诗思考后知道了在小诗这里" + dynasty \
                 + "朝代共收录了" + str(wc_cnt) + "篇作品。小诗认为非常著名的 " \
                 + str(limit) + " 首诗词作品如下所示：\n"

        for wc in work_content:
            answer += wc

        print(answer)
        return answer

    # 注意，由于数据库存放的作品数量达到30W以上，所以顺序返回再处理，所需时间较长，所以选择读文件输出
    answer = "哎呀，您的问题还有点复杂呢，小诗思考后知道了在小诗这里" + dynasty \
             + "朝代共收录了" + str(wc_cnt) + "篇作品。小诗认为非常著名的 " \
             + str(limit) + " 首诗词作品如下所示：\n"
    cnt = 1
    for author in sorted_author_of_dynasty[dynasty]:  # 从知名作家开始排序输出, 如从唐代李白、白居易、杜甫开始
        author_cnt = 1
        for sorted_work in sorted_work_of_author[author]:  # 从知名作者的知名作品开始
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
        """

    # 18 - work_of_type_1
    """
    work_type = "思乡"

    cypher = "match (wt:WorkType{name:'%s'})<-[r:type_is]-(wc:WorkContent)" \
             " return count(wc)" % work_type
    work_cnt = graph.run(cypher).data()[0].get('count(wc)')  # 数据库中该类型收录的作品的数量

    cypher = "match (wt:WorkType{name:'%s'})<-[r:type_is]-(wc:WorkContent)" \
             " return wc.title, wc.author, wc.content, wc.dynasty" % work_type
    results = graph.run(cypher).data()  # 数据库中该朝代作者的数量

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
    answer = "小诗刚刚在学习古诗词呢，您的问题这就回答您。关于" + work_type \
             + "类型的古诗词作品小诗一共学习了" + str(work_cnt) + \
             "篇。给您推荐其中著名的 " + str(limit) + " 篇，分别如下所示：\n"
    cnt = 1
    for author, works in sorted_work_of_author.items():
        if author in work_of_author:
            for work in work_of_author[author]:
                title = work[0]
                dynasty = work[1]
                content = work[2]
                if content != "暂未收录":
                    # 输出需加工
                    sent_len = len(content.split("\n")[0])
                    sent_format = "{0:^" + str(sent_len) + "}"
                    answer += sent_format.format(title) + "\n" + \
                              "{0:>8}·{1:<8}".format(dynasty, author) + '\n' + content + '\n'
                    cnt += 1

            if cnt > limit:
                break
    """

    # 19 - fs_of_type_1
    """
    fs_type = "爱国"

    cypher = "match (wt:WorkType{name:'%s'})<-[r:type_is]-(fs:FamousSentence)" \
             " return count(fs)" % fs_type
    fs_cnt = graph.run(cypher).data()[0].get('count(fs)')  # 数据库中该类型收录的作品的数量

    cypher = "match (wt:WorkType{name:'%s'})<-[r:type_is]-(fs:FamousSentence)" \
             " return fs.title, fs.author, fs.content" % fs_type
    results = graph.run(cypher).data()  # 数据库中该朝代作者的数量

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
    answer = "小诗可是古诗词领域的铁粉呢，马上回答您。关于" + fs_type \
             + "类型的古诗词佳句小诗一共了解" + str(fs_cnt) + \
             "条。给您推荐其中著名的 " + str(limit) + " 句，它们分别是：\n"
    cnt = 1
    for author, works in sorted_work_of_author.items():
        if author in fs_of_author:
            author_cnt = 1
            for work in fs_of_author[author]:
                if author_cnt > 10:  # 每个作者最多输出10条
                    break

                title = work[0]
                content = work[1]
                # 输出需加工
                answer += content + "————" + author + "《" + title + "》" + "\n"
                author_cnt += 1
                cnt += 1

        if cnt > limit:
            break"""

    # 20 - type_of_work_1
    """    title = "静夜思"
    # 首先需要知道该标题对应了多少作品
    cypher = "match(wc:WorkContent) -[r:title_is]-> (wt:WorkTitle{name: '%s'})" \
             " return count(wc)" % title
    work_cnt = graph.run(cypher).data()[0].get('count(wc)')  # 数据库中该朝代作者的数量

    if work_cnt == 0:  # 表示作品不存在，或者该作品分辨不出类型来
        return answer
    elif work_cnt == 1:  # 该标题只对应一个作品
        cypher = "match (wc:WorkContent{title:'%s'}) -[r:type_is]-> (wt:WorkType) " \
                 " return wt.name " % title
        results = graph.run(cypher).data()  # 该作品的类型数量

        if not results:  # 该作品虽然在知识图谱中，但是还不知道它的类型
            answer = "太抱歉了，小诗目前还不知道《" + title + "》这一作品的类型呢，但是我会继续学习的，争取早日知道。\n"
            return answer

        answer = "古诗词领域的博才小诗，当然能够问答你的问题啦。" \
                 + "从作品《" + title + "》" + "的内容来看，小诗将其类型归类为："

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
        results = graph.run(cypher).data()
        title_works = {}
        for result in results:
            author = result.get('wc.author')
            dynasty = result.get('wc.dynasty')
            content = result.get('wc.content')
            title_works[author] = (dynasty, content)

        answer = "古诗词领域的博才小诗，当然能够问答你的问题啦。" \
                 + "小诗目前了解到有" + str(work_cnt) + "篇诗词作品的标题为《" + title + "》，" + "我将分别呈现给你哟。\n"

        # 然后分别查好对应的作品，输出相关的类型
        cnt = 1
        for author, work in title_works.items():
            cypher = "match (wc:WorkContent{title:'%s', author:'%s'}) -[r:type_is]-> (wt:WorkType) " \
                     " return wt.name " % (title, author)
            results = graph.run(cypher).data()  # 该作品的类型数量
            dynasty, content = work[0], work[1]
            answer += "第" + str(cnt) + "篇诗词作品的内容如下所示：\n"
            answer += "{0:^16}".format(title) + "\n" + \
                      "{0:>8}·{1:<8}".format(dynasty, author) + '\n' + content

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

            cnt += 1"""

    # 21 - type_of_fs_1
    """
    fs = "为君题，惜解携。"
    # 首先需要知道该标题对应了多少作品
    cypher = "match(fs:FamousSentence{content: '%s'}) -[r:type_is]-> (wt:WorkType)" \
             " return wt.name, fs.author, fs.dynasty, fs.title" % fs
    results = graph.run(cypher).data()

    if not results:   # 找不到名句
        answer = "非常抱歉，小诗的学识还有待提高呢。这一著名的诗句，小诗目前还不能知道它的所属类型呢。"
        return answer

    title = results[0].get("fs.title")
    author = results[0].get("fs.author")
    dynasty = results[0].get("fs.dynasty")

    answer = "这个问题你找小诗就是找对啦，我可博学多才呢。" \
                 + "小诗目前了解到，著名佳句“" + fs + "”" + "是" +\
             dynasty + "的著名诗词作家" + author + "在其作品《" + title + "》中写的。" + \
                "从这句的内容来看，小诗将其类型归类为："

    type_cnt = len(results)
    if type_cnt == 1:
        answer += results[0].get('wt.name') + "类。"
    else:
        for i in range(type_cnt):
            if i == type_cnt - 1:
                answer += "和" + results[i].get('wt.name') + "类。"
            else:
                answer += results[i].get('wt.name') + "类、"
    """

    # 22 - fs_of_work_1
    """
    title = "静夜思"

    # 首先查找该作品是否存在于数据库
    cypher = "match (wc: WorkContent{title: '%s'}) return wc" % title
    results = graph.run(cypher).data()
    if not results:
        answer = "非常抱歉，小诗的学识还有待提高呢，小诗目前没有学过作品《" + title + "》" + "。"
        return answer

    # 作品存在数据库中
    cypher = "match(wc: WorkContent{title: '%s'}) -[r:include]-> (fs:FamousSentence)" \
             " return wc.content, fs.author, fs.dynasty, fs.content" % title
    results = graph.run(cypher).data()

    if not results:  # 作品存在数据库中，但是找不到名句
        answer = "非常抱歉，小诗的学识还有待提高呢。小诗目前还不知道作品《" +\
                 title + "》" + "有哪些名句哟，等我继续学习之后再回答你。"
        return answer

    content = results[0].get("wc.content")  # 作品内容
    author = results[0].get("fs.author")
    dynasty = results[0].get("fs.dynasty")

    answer = "这题我会，难不倒我智能小诗。它的内容如下所示：\n" + "{0:^16}".format(title) + "\n" + \
                              "{0:>8}·{1:<8}".format(dynasty[0], author) \
             + '\n' + content + '\n' + '小诗目前了解到该作品包括如下名句：\n'

    type_cnt = len(results)
    if type_cnt == 1:
        answer += "“" + results[0].get('fs.content') + "”" + '\n'
    else:
        for i in range(type_cnt):
            answer += "第 " + str(i + 1) + " 句 ———— " + results[i].get('fs.content') + '\n'
    """

    # 23 - author_of_ct_1
    """
    collective_title = "唐宋八大家"

    # 首先查找识别出来的合称是否存在于数据库
    cypher = "match (ct: CollectiveTitle{name: '%s'}) return ct" % collective_title
    results = graph.run(cypher).data()

    if not results:
        answer = "非常抱歉，小诗的学识还有待提高，合称“" + collective_title + "”目前我还不知道指的哪些诗词作家呢。"
        return answer

    # 作品存在数据库中
    cypher = "match (a: Author) -[r:collective_title]-> (ct: CollectiveTitle{name: '%s'})" \
             " return a.name, a.dynasty" % collective_title
    results = graph.run(cypher).data()

    answer = "好累呀，小诗最近一直在学习古诗词领域的知识呢，你的这个问题可难不倒我。\n合称”" \
             + collective_title + "“" + "所指的是 ———— "
    rel_len = len(results)
    for i in range(rel_len):
        author = results[i].get('a.name')
        dynasty = results[i].get('a.dynasty')
        if i == rel_len - 1:
            answer += "以及" + dynasty + "的" + author + "。"
        else:
            answer += dynasty + "的" + author + "、" """

    # 24 - author_of_female_1
    """
    gender = "女"
    if gender == "男":
        answer = "这个问题小诗可不可以跳过呢，因为我国古代的男性诗人、词人实在是太多啦，但是你可以让我" \
                 "列举我国古代著名的女性诗词作家呢。"
        return answer

    cypher = "match (a: Author) -[r: gender_is]-> (g: Gender{name: '%s'}) " \
             "return a.name, a.dynasty" % gender
    results = graph.run(cypher).data()

    cypher = "match (a: Author) -[r: gender_is] -> (g :Gender{name: '%s'}) return count(a)" % gender
    author_cnt = graph.run(cypher).data()[0].get("count(a)")

    answer = "经过小诗废寝忘食地学习，你的这个问题我可以回答哦。我国古代著名的女性诗词作家" \
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
            """

    # 25 - work_of_title_1
    """
    title = "春望"

    # 首先判断该作品是否在数据库里
    cypher = "match (wt: WorkTitle{name: '%s'}) return wt" % title
    result = graph.run(cypher).data()

    if not result:
        answer = "实在太抱歉啦，小诗目前还没有学过《" + title + "》" + "这篇作品呢，我会继续学习的。"
        print(answer)
        return answer

    cypher = "match (wt: WorkTitle{name: '%s'}) <-[r: title_is]-" \
             " (wc: WorkContent) return wc.author, wc.dynasty, wc.content" % title
    results = graph.run(cypher).data()
    work_cnt = len(results)

    answer = "小诗博览全书，学到了很多古诗词领域的知识呢，标题为《" + title \
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
    """

    # 26 - type_work_dynasty_1
    """
    dynasty = "唐朝"

    if dynasty in aligning_dict:  # 各朝代对齐
        dynasty = aligning_dict[dynasty]

    work_type = "田园"

    # 首先判断该作品是否在数据库里
    cypher = "match (wc: WorkContent{dynasty: '%s'}) -[r: type_is]-> " \
             "(wt: WorkType{name: '%s'}) return wc.author, wc.title, wc.content" % (dynasty, work_type)
    results = graph.run(cypher).data()

    if not results:
        answer = "不好意思，虽然小诗博览群书，但是创作于" + dynasty + "的关于" \
                 + work_type + "类型的诗词作品，小诗目前还没有学习到呢，但是小诗会继续学习的。\n"
        print(answer)
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

    answer = "虽然你的问题比较复杂，但是小诗仍旧可以回答呢。创作于" + dynasty + "且关于" \
             + work_type + "类型的诗词作品，小诗目前一共了解了" \
             + str(work_cnt) + "篇，其中非常著名的"

    cnt = 1
    tmp_answer = ""
    for author in sorted_author_of_dynasty[dynasty]:
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
    answer += str(cnt) + "篇如下所示：\n" + tmp_answer"""

    # 27 - dynasty_author_female_1
    """
    dynasty = "未知"

    if dynasty in aligning_dict:  # 各朝代对齐
        dynasty = aligning_dict[dynasty]

    gender = "女"
    if gender == "男":
        answer = "这个问题小诗可不可以跳过呢，因为" + dynasty + "的男性诗人、词人实在是太多啦，但是你可以让我" \
                 "列举该时期的女性诗词作家呢。"
        return answer

    # 首先判断该作品是否在数据库里
    cypher = "match (a:Author{gender: '%s'}) -[r:belong_to]->" \
             " (d: Dynasty{name: '%s'}) return a.name" % (gender, dynasty)
    results = graph.run(cypher).data()

    if not results:
        answer = "哎呀，很抱歉啦。目前，小诗还不知道" + dynasty + "有哪些著名的女性诗词作家呢。\n"
        return answer

    work_cnt = len(results)
    answer = "这个话题小诗非常感兴趣，目前小诗了解到，" + dynasty + "一共有" \
             + str(work_cnt) + "位著名的女性诗词作家。她们分别是 ———— "

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
    """

    # 28 - author_type_work_1
    """
    author = "李白"
    work_type = "写景"

    # 首先判断该作者是否在数据库里
    cypher = "match (a: Author{name: '%s'}) return a" % author
    results = graph.run(cypher).data()

    if not results:
        answer = "非常抱歉，目前小诗还不认识" + author + "这位作家呢，但是我会去了解的。\n"
        return answer

    cypher = "match (wc: WorkContent{author: '%s'}) - [r: type_is] ->" \
             " (wt: WorkType{name: '%s'}) return wc.title, wc.dynasty, wc.content" % (author, work_type)
    results = graph.run(cypher).data()
    work_cnt = len(results)

    if work_cnt == 0:
        answer = "虽然小诗专注于古诗词领域，但是目前并没有了解到" + author\
                 + "是否写过哪些关于" + work_type + "类型的作品呢。"
        return answer

    answer = "还没遇见你时，小诗一直都在努力学习，你的问题我肯定能问答啦。" + \
             "著名诗词作家" + author + "一共创作了" + str(work_cnt) \
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
        """

    # 29 - author_type_fs_1
    """
    author = "李白"
    work_type = "爱情"

    # 首先判断该作者是否在数据库里
    cypher = "match (a: Author{name: '%s'}) return a" % author
    results = graph.run(cypher).data()

    if not results:
        answer = "非常抱歉，目前小诗还不认识" + author + "这位作家呢，但是我会去了解的。\n"
        return answer

    # 匹配作者和对应类型的诗句
    cypher = "match (fs: FamousSentence{author: '%s'}) - [r: type_is] ->" \
             " (wt: WorkType{name: '%s'}) return fs.title, fs.dynasty, fs.content" % (author, work_type)
    results = graph.run(cypher).data()
    fs_cnt = len(results)

    if fs_cnt == 0:
        answer = "虽然小诗专注于古诗词领域，但是目前并没有了解到" + author \
                 + "是否写过哪些关于" + work_type + "类型的名句呢。"
        return answer

    answer = "小诗觉得这个问题不是很难，毕竟我在古诗词领域学习很长时间了。" + \
             "著名诗词作家" + author + "在其创作的作品中，一共包含了" + str(fs_cnt) \
             + "句关于" + work_type + "类型的著名佳句呢，分别如下所示：\n"

    for result in results:  # 便于按照热度排序后输出
        title = result.get('fs.title')
        content = result.get('fs.content')
        answer += content + " ———— " + author + "《" + title + "》\n"
    """

    # 30 - author_work_type_1
    """
    author = "苏轼"
    title = "赤壁赋"  # 春望

    # 首先判断该作者是否在数据库里
    cypher = "match (a: Author{name: '%s'}) return a" % author
    results = graph.run(cypher).data()

    if not results:
        answer = "非常抱歉，目前小诗还不认识" + author + "这位作家呢，但是我会去了解的。\n"
        return answer

    # 判断作者是否写过某作品
    cypher = "match (wc: WorkContent) where wc.author='%s' and wc.title='%s' return wc" % (author, title)
    result = graph.run(cypher).data()
    if not result:
        answer = "哎呀，在小诗的印象里，" + author + "的所有诗词作品中好像并没有《" + \
                 title + "》这篇作品呢。但是，你可以去问问我的好朋友们，比如小度、小艺和小爱同学。"
        return answer

    # 匹配作者和对应标题的作品
    cypher = "match (wc: WorkContent{author: '%s', title: '%s'}) - [r: type_is] ->" \
             " (wt: WorkType) return wt.name, wc.dynasty, wc.content" % (author, title)
    results = graph.run(cypher).data()
    type_cnt = len(results)

    if type_cnt == 0:
        answer = "虽然小诗专注于古诗词领域，但是目前并不知道" + author \
                 + "的《" + title + "》属于什么类型的诗词作品呢。\n"
        return answer

    answer = "小诗，在古诗词领域了解了很多关于作者、作品和名句相关的知识。最近刚刚了解了" + \
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

    print(answer)
    """

    # 31 - author_of_wc_1
    """
    work_cnt = str(100)  # 春望

    # 首先判断该作者是否在数据库里
    cypher = "match (a: Author) where a.work_cnt > '%s' return a.name" % work_cnt
    results = graph.run(cypher).data()

    author_cnt = len(results)
    if author_cnt > 20:
        limit = 20
    else:
        limit = author_cnt

    answer = "小诗非常热衷于古诗词领域的各类知识呢，我所知道的作者他们的作品数量达到" + work_cnt \
             + "的诗词作家一共有" + str(author_cnt) + "位，小诗列出" + str(limit) + "位，如下所示：\n"
    for i in range(limit):
        if i == limit - 1:
            answer += "和" + results[i].get('a.name') + '。'
        elif i == limit - 2:
            answer += results[i].get('a.name')
        else:
            answer += results[i].get('a.name') + '、'

    print(answer)
    """

    # 32 - author_2
    """
    author = "姚源杰"  # 获取问句的实体 - 取第一个实体回答
    cypher = "match (a: Author{name: '%s'}) return a.gender, a.dynasty, a.work_cnt" % author
    result = graph.run(cypher).data()  # 获取第一组结果

    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        answer = "非常抱歉啦，小诗目前了解到" + author + "并不是一个诗词作家哦，" \
                        "如果你不放心，可以去咨询一下我的好朋友小艺呢。\n"
        print(answer)
        return answer

    dynasty, gender, work_cnt = result[0].get('a.dynasty'), result[0].get('a.gender'), result[0].get(
        'a.work_cnt')

    if gender == '男':
        slot = '他'
    else:
        slot = '她'

    answer = "是的，" + author + "是我国" + dynasty + "时期的著名诗词作家" + slot \
             + "一生创作了" + str(work_cnt) + "篇的文学作品呢。\n"   """

    # 33 - gender_of_author_2
    """
    author = "李清照"
    gender = "女"

    cypher = "match (a: Author{name: '%s'}) return a.gender, a.dynasty" % author
    result = graph.run(cypher).data()  # 获取第一组结果

    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        answer = "非常抱歉啦，小诗目前还不认识" + author + "，但是你可以去咨询一下我的好朋友小艺呢。\n"
        print(answer)
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
    """

    # 34 - dynasty_of_author_2
    """
    author = "李白"
    dynasty = "宋朝"

    if dynasty in aligning_dict:
        dynasty = aligning_dict[dynasty]
    else:
        answer = "太抱歉了，目前小诗还不知道有" + dynasty + "的存在呢。\n"
        return answer

    cypher = "match (a: Author{name: '%s'}) return a.gender, a.dynasty, a.work_cnt" % author
    result = graph.run(cypher).data()

    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        answer = "非常抱歉啦，小诗目前还不认识" + author + "，但是你可以去咨询一下我的好朋友小艺呢。\n"
        print(answer)
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
    
    """

    # 35 - author_of_fs_2
    """
    author = "李白"
    fs = "举头望明月，低头思故乡。"

    # 首先判断作者是否在知识图谱里
    cypher = "match (a: Author{name: '%s'}) return a" % author
    result = graph.run(cypher).data()
    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        answer = "非常抱歉啦，小诗目前还不认识" + author + "，但是你可以去咨询一下我的好朋友小艺呢。\n"
        print(answer)
        return answer

    # 然后判断坐着是否写过该名句
    cypher = "match (a: Author{name: '%s'}) -[r: write]-> (fs: FamousSentence{content: '%s'}) " \
             "return a.gender, fs.title, fs.dynasty " % (author, fs)
    result = graph.run(cypher).data()

    if not result:  # 不是该作者写的
        answer = "虽然小诗才高八斗，但我并不知道" + author + "写过名句 ———— “" \
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
                 dynasty + "著名诗词作家" + author + "写的呢，并且是" +\
                 slot + "创作的诗词作品《" + title + "》里的一句哦。"
    """

    # 36 - author_of_work_2
    """
    author = "李白"
    title = "赤壁赋"

    # 首先判断作者是否在知识图谱里
    cypher = "match (a: Author{name: '%s'}) return a" % author
    result = graph.run(cypher).data()
    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        answer = "非常抱歉啦，小诗目前还不认识" + author + "，但是你可以去咨询一下我的好朋友小度呢。\n"
        print(answer)
        return answer

    # 然后判断坐着是否创作了该作品
    cypher = "match (a: Author{name: '%s'}) -[r: create]-> (wc: WorkContent{title: '%s'}) " \
             "return a.gender, a.dynasty, wc.content " % (author, title)
    result = graph.run(cypher).data()

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
                 "。" + slot + "创作的这篇作品的内容如下所示：\n" +\
                 "{0:^16}".format(title) + "\n" + "{0:>8}·{1:<8}".format(dynasty[0], author)\
                 + "\n" + content + '\n'
    """

    # 37 - type_of_work_2
    """
    title = "赤壁赋"
    work_type = "哲理"

    # 首先判断作品是否在知识图谱里
    cypher = "match (wc: WorkContent{title: '%s'}) return wc" % title
    results = graph.run(cypher).data()
    if not results:  # 知识图谱中找不到匹配，则返回默认的答案
        answer = "十分不好意思，小诗目前还没有学习过《" + title + "》这篇作品呢，但是我会尽快去学的。\n"
        print(answer)
        return answer

    # 然后判断作品的类型
    cypher = "match (wc: WorkContent{title: '%s'}) -[r: type_is]-> (wt: WorkType) " \
             "return wc.author, wc.dynasty, wc.content, wt.name" % title
    results = graph.run(cypher).data()

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
    """

    # 38 - author_of_ct_2
    """
    collective_title = "唐宋八大家"
    authors = ["苏轼", "苏洵"]

    # 首先判断合称是否在知识图谱里
    cypher = "match (ct: CollectiveTitle{name: '%s'}) return ct" % collective_title
    result = graph.run(cypher).data()
    if not result:  # 知识图谱中找不到匹配，则返回默认的答案
        answer = "非常抱歉啦，虽然小诗了解过很多诗词名家的合称，但是目前还不知道合称“" \
                 + collective_title + "“的存在呢。\n"
        print(answer)
        return answer

    # 然后判断合称包含的作者
    cypher = "match (ct: CollectiveTitle{name: '%s'}) <-[r: collective_title]-" \
             " (a: Author) " \
             "return a.name, a.dynasty" % collective_title
    results = graph.run(cypher).data()

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

        answer = "并非像你描述的那样哦，在小诗看来，" + collective_title\
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
    """

    # 39 - wc_of_author_3
    """
    authors = ['李白', '杜甫']

    # 首先判断两作者是否在知识图谱中
    flag = True
    for author in authors:
        cypher = "match (a: Author{name: '%s'}) return a" % author
        if not graph.run(cypher).data():
            flag = False

    if not flag:  # 不存在这些作者
        answer = "不好意是，在小诗的学习过程中，我并没有了解过这些诗词作家，但是你可以去咨询我的好朋友天猫精灵哦。\n"
        return answer

    # 开始比较两者的情况
    cypher = "match (a1: Author{name: '%s'}), (a2: Author{name: '%s'}) " \
             "return a1.work_cnt > a2.work_cnt, a1.work_cnt, a2.work_cnt" % (authors[0], authors[1])

    result = graph.run(cypher).data()[0]
    judge = result.get('a1.work_cnt > a2.work_cnt')  # 布尔型

    if judge:  # author_cnt1 > author_cnt2
        work_cnt_1, work_cnt_2 = int(result.get('a1.work_cnt')), int(result.get('a2.work_cnt'))
        answer = "是的没错，小诗了解到，" + authors[0] + "一生创作了" \
                 + str(work_cnt_1) + "篇作品，而" + authors[1]\
                 + '一生创作了' + str(work_cnt_2) + "篇作品。所以，" +\
                 authors[0] + "的作品数量比" + authors[1] + "的作品数量多，多了" \
                 + str(work_cnt_1 - work_cnt_2) + "篇呢。\n"
    else:
        work_cnt_1, work_cnt_2 = int(result.get('a1.work_cnt')), int(result.get('a2.work_cnt'))
        answer = "并不是这样的，小诗了解到，" + authors[0] + "一生创作了" \
                 + str(work_cnt_1) + "篇作品，而" + authors[1] \
                 + '一生创作了' + str(work_cnt_2) + "篇作品。所以，" + \
                 authors[0] + "的作品数量比" + authors[1] + "的作品数量少，少了" \
                 + str(work_cnt_2 - work_cnt_1) + "篇呢。\n"
    print(answer)
    """

    # 40 - max_wc_3
    """
    cypher = "match (a: Author) return a.work_cnt, a.dynasty, a.name, a.gender"
    results = graph.run(cypher).data()
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

    answer = "那怎么说小诗这么聪明呢，这个问题我可知道哟。我国古代创作最多的作者是" \
             + author['max'][2] + "的" + author['max'][0] + "，" + slot\
             + "一共创作了" + str(max_cnt) + "篇作品呢。\n"
    print(answer)"""

    # 41 - dynasty_of_author_3
    """
    authors = ['王安石', '杜甫']

    # 首先判断两作者是否在知识图谱中
    flag = True
    for author in authors:
        cypher = "match (a: Author{name: '%s'}) return a" % author
        if not graph.run(cypher).data():
            flag = False

    if not flag:  # 不存在这些作者
        answer = "不好意是，在小诗的学习过程中，我并没有了解过这些诗词作家，但是你可以去咨询我的好朋友小艺哦。\n"
        return answer

    # 开始比较两者的情况
    cypher = "match (a1: Author{name: '%s'}), (a2: Author{name: '%s'}) " \
             "return a1.dynasty=a2.dynasty, a1.dynasty, a2.dynasty" % (authors[0], authors[1])

    result = graph.run(cypher).data()[0]
    judge = result.get('a1.dynasty=a2.dynasty')  # 布尔型

    if judge:  # 两作者的朝代相同
        answer = "是的呢，小诗可以确定，" + authors[0] + "和" \
                 + authors[1] + "都是" + result.get('a1.dynasty') + "的著名诗词作家呢。\n"
    else:
        answer = "不对哦，小诗了解到，" + authors[0] + "出生于" \
                 + result.get('a1.dynasty') + "，而" + authors[1] + "出生在" + result.get('a2.dynasty') + "呢。\n"
    """

    # 42 - cnt_of_author_3
    """
    dynasties = ['唐朝', '宋代']

    for i in range(2):  # 朝代对齐
        if dynasties[i] not in aligning_dict:
            answer = "抱歉，小诗目前还不知道朝代“" + dynasties[i] + "”的存在呢。\n"
            return answer
        else:
            dynasties[i] = aligning_dict[dynasties[i]]

    cypher1 = "match (a1: Author{dynasty: '%s'})  return count(a1)" % dynasties[0]
    cypher2 = "match (a2: Author{dynasty: '%s'})  return count(a2)" % dynasties[1]
    cnt_1 = graph.run(cypher1).data()[0].get('count(a1)')
    cnt_2 = graph.run(cypher2).data()[0].get('count(a2)')

    judge = cnt_1 > cnt_2
    if judge:  # 前者大于后者
        answer = "这个问题很简单哦，据小诗不完全统计，" + dynasties[0] + "一共有" \
                 + str(cnt_1) + "位著名的诗词作家，而" + dynasties[1]\
                 + "一共有" + str(cnt_2) + "位著名的诗词作家，" \
                 + "所以前者多于后者哦。\n"
    else:
        answer = "这个问题很简单哦，据小诗不完全统计，" + dynasties[0] + "一共有" \
                 + str(cnt_1) + "位著名的诗词作家，而" + dynasties[1] \
                 + "一共有" + str(cnt_2) + "位著名的诗词作家，" \
                 + "所以后者多于前者哦。\n"
    """

    print(answer)


def test():
    # 连接时指定name
    graph = Graph("bolt://localhost:7687"  # http://127.0.0.1:7474
                  , auth=("neo4j", "******"), name='poetry')  # 用户名和密码按实际情况更改
    query(graph)


if __name__ == '__main__':
    # 清空数据库 MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r
    test()
