# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/4/10 13:22
 @Author: Glimmering
 @Function: 系统启动
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 将父文件夹加入根路径，防止导包出错

import json
import markdown
import requests
import config
from exts import db, mail
from models import UserModel  # 导入模型
from blueprints.prefix import bp as prefix_bp
from flask_migrate import Migrate
from decorators import login_required

from flask import Flask, render_template, request, jsonify, session, g, Response  # g 全局 session, g  # g 全局
from KGQA.kgqa_hlm.query_graph import query, get_KGQA_answer, get_answer_profile
from KGQA.kgqa_hlm.ltp import get_target_array
from KGQA.xiaoshi_robot import XiaoShiRobot
from KGQA.query_poetry import query_author_work

app = Flask(__name__)

# 绑定配置文件
# app.config.from_object(config)

# # 从配置文件中settings加载配置
app.config.from_pyfile('config.py')
app.config['JSON_AS_ASCII'] = False

# mysql数据库的初始化
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)
# ORM 模型映射成表的三步
# 1. flask db init  只需执行一次fl
# 2. flask db migrate 识别ORM模型的改变，生成迁移脚本
# 3. flask db upgrade 运行迁移脚本，同步到数据库中


# 绑定蓝图  blueprint: 用来做模块化的
app.register_blueprint(prefix_bp)


# 1 - 首页
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    return render_template('index.html', name=name)


# 2 - 人物实体及关系搜索 - 红楼梦
@app.route('/search', methods=['GET', 'POST'])
@login_required   # 登录验证
def search():
    return render_template('search.html')


# 3 - 获取所有关系 前端展示知识图谱 - 红楼梦
@app.route('/get_relations', methods=['GET', 'POST'])
@login_required   # 登录验证
def get_relations():
    return render_template('relations.html')


# 4 - 知识图谱问答系统页面 - 红楼梦
@app.route('/KGQA', methods=['GET', 'POST'])
@login_required   # 登录验证
def KGQA():
    return render_template('KGQA.html')


# 5 - 获取人物的简介 - 红楼梦
@app.route('/get_profile', methods=['GET', 'POST'])
def get_profile():
    name = request.args.get('character_name')
    json_data = get_answer_profile(name)
    return jsonify(json_data)


# 6 - 基于知识图谱的问答 - 红楼梦
@app.route('/KGQA_Answer', methods=['GET', 'POST'])
def KGQA_Answer():
    question = request.args.get('name')  # js 获取前端输入的问题: 贾宝玉的父亲是谁
    target_array = get_target_array(str(question))
    json_data = get_KGQA_answer(target_array)
    return jsonify(json_data)


# 7 - 图谱中搜索姓名 - 红楼梦
@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query(str(name))
    return jsonify(json_data)


# 8 - 知识图谱问答系统页面 - 古诗词
@app.route('/KGQA_Poetry', methods=['GET', 'POST'])
@login_required   # 登录验证
def KGQA_Poetry():
    return render_template('KGQA_Poetry.html')


# 9 - 基于知识图谱的问答 - 古诗词
@app.route("/KGQA_Poetry_Answer", methods=["POST"])
def KGQA_Poetry_Answer():
    # 古诗词领域问答
    list_str = request.form.get("prompts", None)

    answer_list = json.loads(list_str)
    question = answer_list[-1]['content']  # 获取前端输入的问题: 李白写过哪些诗啊？
    xiaoshi_robot = XiaoShiRobot(question)
    answer = xiaoshi_robot.answer()
    answer = answer.replace("\n", "<br>")   # 便于前端展示
    return markdown.markdown(answer)   # 转换成 markdown模式


# 10 - 作者与作品的搜索 - 古诗词
@app.route('/search_poetry', methods=['GET', 'POST'])
@login_required   # 登录验证
def search_poetry():
    return render_template('search_poetry.html')


# 11 - 图谱中搜索作品和作者 - 古诗词
@app.route('/search_author_work', methods=['GET', 'POST'])
def search_author_work():
    name = request.args.get('name')
    # print(name)
    json_data = query_author_work(str(name))
    return jsonify(json_data)


# 12 - hook 钩子函数，登录验证
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


# 13 - 上下文处理器，登录验证
@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.debug = True
    app.run()
