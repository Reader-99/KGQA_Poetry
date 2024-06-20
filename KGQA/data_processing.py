"""
 coding=utf-8
 @Software: PyCharm
 @Date: 2024/3/14 14:59
 @Author: Glimmering
 @Function: 用户意图为：聊天问答
"""
import json


# 1 - jieba 字典去重
def jieba_dict():
    path = './user_dict/jieba_dict.txt'
    lines = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line not in lines:
                lines[line] = 1
            else:
                # print(line, end='')
                lines[line] += 1

        f.close()

    path = './user_dict/dict.txt'
    with open(path, 'w', encoding='utf-8') as f:
        for line, cnt in lines.items():
            if cnt > 1:
                print(line, end='')
            f.write(line)

        f.close()


# 2 - 作者排序
def sorted_authors():
    aligning_dynasty = {"唐代": "唐代", "宋代": "宋代", "清代": "清朝", "魏晋": "魏晋",
                        "五代": "五代", "两汉": "两汉", "先秦": "先秦", "元代": "元朝",
                        "南北朝": "南北朝", "明代": "明代", "隋代": "隋朝", "金朝": "金朝",
                        "未知": "未知", "近代": "近现代", "现代": "近现代"}

    authors = {}
    dynasties = {}
    path = './sorted_poems/hot_authors.txt'
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            author = line.split('@')[0]
            dynasty = line.split('@')[1].split('\t')[0]
            hot = line.split('@')[1].split('\t')[1].split('\n')[0]

            if author not in authors:
                authors[author] = int(hot) + 1
            else:
                print(author)

            dynasty = aligning_dynasty[dynasty]
            if dynasty not in dynasties:
                dynasties[dynasty] = [author]
            else:
                dynasties[dynasty].append(author)

        f.close()
    path = './sorted_poems/hot_authors.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(authors, f, indent=4, ensure_ascii=False)
        f.close()

    path = './sorted_poems/sorted_dynasty_authors.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dynasties, f, indent=4, ensure_ascii=False)
        f.close()

    # print(authors)
    # print(dynasties)


# 3 - 诗词排序
def sorted_poems():
    works = {}
    authors = {}
    path = './sorted_poems/hot_works.txt'
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            # print(line)
            author = line.split('@')[0]
            author_title = line.split('\t')[0]
            title = line.split('@')[1].split('\t')[0]
            hot = line.split('@')[1].split('\t')[1].split('\n')[0]

            if author_title not in works:
                works[author_title] = int(hot)
            else:
                print(author_title)

            if author not in authors:
                authors[author] = [title]
            else:
                authors[author].append(title)

        f.close()

    path = './sorted_poems/hot_works.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(works, f, indent=4, ensure_ascii=False)
        f.close()

    path = './sorted_poems/sorted_author_works.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(authors, f, indent=4, ensure_ascii=False)
        f.close()

    # print(authors)
    # print(dynasties)


# 20 - 数据处理
def data_processing():
    # sorted_authors()
    sorted_poems()


if __name__ == "__main__":
    data_processing()