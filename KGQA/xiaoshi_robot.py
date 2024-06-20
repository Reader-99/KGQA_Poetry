# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/29 15:11
 @Author: Glimmering
 @Function: 有关古诗词领域问题的问答智能机器人 - 小诗
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 将父文件夹加入根路径，防止导包出错
from .kgqa_nlu import NaturalLanguageUnderstanding  # 自然语言理解
from .kgqa_nlg import NaturalLanguageGeneration  # 自然语言生成
from .kgqa_config import configs


class XiaoShiRobot:
    __doc__ = "智能古诗词问答机器人 - 小诗"

    def __init__(self, question):
        self.question = question
        self.logger = configs['logger']

    # 1 - 返回问答结果
    def answer(self):
        nlu = NaturalLanguageUnderstanding(self.question, self.logger)
        intent, entities = nlu.intent_classification()  # 获取用户意图与问句中的实体
        nlg = NaturalLanguageGeneration(intent, entities)
        answer_of_question = nlg.answer_generation()
        # self.logger.info(answer_of_question)
        return answer_of_question


if __name__ == "__main__":
    """ 意图类型1 - 对比型问句"""
    # question = "我对苏轼的文学影响与其弟子们的文学贡献感兴趣，能否告诉我苏门四学士的身份？"
    # question = "小诗，你现在能够为我提供帮助吗？如果可以，我想听一听你关于李白这位伟大诗人的见解。"
    # question = "哈喽，我想知道更多与作品《静夜思》相关的信息，你能告诉我吗？"
    # question = "小诗，你记得“两个黄鹂鸣翠柳，一行白鹭上青天”这句在哪里出现过吗？"
    # question = "上午好，小诗，你确定无疑地知道李白是男性还是女性，对吧？"
    # question = "小诗，我对苏轼的诗词内涵极为赞赏，你能否告诉我他所属的历史时代？"
    # question = "哈喽，小诗！我特别想弄清楚李白创作的所有诗歌作品加起来有多少首？"
    # question = "近来我沉浸于《江城子其一》的氛围之中，小诗，你能否告诉我这首诗的原创撰稿人是谁？"  # 1
    # question = "哈罗，小诗，你是否了解《静夜思》的创作者是何人？若知晓的话，请分享一下，感激不尽。"  # 2
    # question = "我刚刚读了楚女谣的两句诗，但不清楚这首诗的作者是哪个朝代的。"
    # question = "嘻嘻，心情超棒！小诗，我想问问你，静夜思具体写了些什么内容？我知道你无所不知哦！"  # 1
    # question = "嘻嘻，心情超棒！小诗，我想问问你，定风波·莫听穿林打叶声具体写了些什么内容？我知道你无所不知哦！"  # 2
    # question = "小诗，你好，能否确认一下“问君能有几多愁？恰似一江春水向东流”这句诗的原始出处——即其所属诗词的标题？"
    # question = "嘿，小诗，“东临碣石，以观沧海。”这句诗是谁的大作啊？我竟然忘记了。"
    # question = "小诗，你知道张杰唱过的那句“空山新雨后，天气晚来秋”是哪个朝代的诗人留下的吗？"
    # question = "你好！对李煜的词作非常感兴趣，能否分享一下他创作过的所有词的列表？"
    # question = "你好，我在寻找陶渊明那些被世人称颂不已的名篇佳句，能给我讲讲吗？"
    # question = "我对先秦时代的诗人还一无所知，能否给出一个全面的名录？"
    # question = "对于唐代时期那些体现文人士大夫情怀的诗词名句，你有何解读？"
    # question = "您对南北朝时期哪些诗词作品的风格或技巧有特别欣赏？"
    # question = "有没有一些表达爱国之情的古诗可以分享？"
    # question = "小诗，我很感兴趣，你能告诉我哪些古诗词名句是描写友情的？"
    # question = "思念之情涌上心头，小诗，有个问题想请教：你是否知晓《静夜思》所属的诗歌类型？"
    # question = "你是否正在吃午饭，小诗？我突然发现对《赤壁赋》里一些经典诗句印象不深。"
    # question = "你好！请问您是否熟悉“唐宋八大家”这一文坛集体的成员身份？"
    # question = "小诗，你还没睡吗？古代的女诗人都有谁啊？跟我说说看吧。"
    # question = "请问，赤壁赋作为作品题目，都有哪些对应的作品？请告诉我一下。"
    # question = "小诗，你能帮我整理一些宋代的春天诗词吗？"
    # question = "小诗，你现在有空吗？能否简单介绍一下唐朝时期有哪些女性诗人及其代表风格？如果有相关信息，请分享。"
    # question = "小诗，我想知道李白写了哪些表达思乡之情的诗，你能帮我查查吗？"
    # question = "小诗，今天是个好天气，来分享一下你所知的李白荷花诗句吧。"  # 思乡、月亮等
    # question = "小诗，你能快速提醒我一下，李白的赤壁赋属于哪一类诗吗？我一时想不起来了，我很着急。"  # 1
    # question = "你好！请问杜甫在《春望》中所表达的主题属于何种类型？"  # 2
    # question = "小诗你好，你能罗列一下那些创作作品超过两千的诗人吗？"

    """意图类型2 - 是否型问句"""
    # question = "哈喽哈喽，雷军曾经是著名的文学家吗？亲爱的小诗。"  # 1
    # question = "小诗，今天天气真是好极了，李白是否是我们古代文学界中的著名诗人？"  # 2
    # question = "小诗，你正忙着什么？李清照有没有被视为男性诗人？"
    # question = "小诗，你智慧过人，孟浩然是否如我们所知，是唐代的一位著名诗人？"
    # question = "你能告诉我，小诗，那句“举头望明月，低头思故乡”是李白写的没错吧？"
    # question = "小诗，你能告诉我，那句“人间有味是清欢”是不是著名诗人苏轼的呢？"

    # 多轮问答
    # question = "小诗，我被“人间有味是清欢”这句诗深深打动，这是苏轼的创作对吧？" # 1
    # question = "那小诗你知道《浣溪沙·细雨斜风作晓寒》的内容吗？"  # 2

    # question = "小诗，我小时候背诵过《游山西村》，请问这是陆游的作品吗？"
    # question = "小诗，你现在有空吗？我迫切需要求证《赠荷花》这首诗是否以荷花为诗歌的情感触发点和艺术表现载体。"
    # question = "小诗，你能否告诉我王安石和苏轼是否是那个特定文学流派的唐宋八大家之一？我记忆有些混乱。"  # 1
    # question = "小诗，你能否告诉我李白和杜甫是否是那个特定文学流派的唐宋八大家之一？我记忆有些混乱。"  # 2

    """意图类型3 - 对比型问句"""
    # question = "昨日在学诗时，我对陶渊明和李商隐的作品数量进行了对比，小诗，你能给我一个明确的答复吗？谢谢。"
    # question = "在众多文坛巨擘之中，我深感好奇：哪位大师的创作总量独步文坛，超越了所有同行？"
    # question = "好嘞，小诗，来个小调查：李白与苏轼这两位诗词大家，他们的出生时代是否一致呢？这对你来说肯定易如反掌吧？嘻嘻！"
    question = "嗨呀，原来宋代有这么多诗人啊？可是你知道明代的诗人会比宋代的诗人多吗？告诉我呢，小诗"

    # 意图类型4 - 其它类型
    # question = "今天的天气真的太好了吧，你觉得呢？"
    robot = XiaoShiRobot(question)
    answer = robot.answer()
    print(answer)
