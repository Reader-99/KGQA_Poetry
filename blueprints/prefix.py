# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/3/2 11:56
 @Author: Glimmering
 @Function: 系统登录与注册界面
"""

import string
import random
from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash
from exts import mail, db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel, UserModel
from werkzeug.security import generate_password_hash, check_password_hash  # 自动生成加密密码
from .forms import RegisterForm, LoginForm     # 当前 forms

# MVC 框架 model-view-controller
bp = Blueprint("", __name__, url_prefix="/")


# 1 - 用户登录视图，系统登录
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash("邮箱在数据库中不存在！")  # 前端显示错误信息
                return render_template("login.html")

            # cookie: 不适合存储太多的数据，适合存储少量的数据。一般存储登录授权的东西
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for("search_poetry"))
            else:
                flash("账号或密码错误！")
                return redirect(url_for("login"))
        else:
            flash(list(form.errors.keys())[0])  # 前端显示错误信息
            return redirect(url_for("login"))

# GET:从服务器上获取数据， POST：将客户端的数据提交给服务器
# 2 - 用户退出登录视图
@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# 3 - 用户注册视图
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证表单  验证用户提交的邮箱和验证码是否对应且正确
        form = RegisterForm(request.form)  # 自动调用该类的验证方法
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            error = list(form.errors.values())[0]  # 字典 转 列表
            flash(error[0])  # 前端显示错误信息
            return redirect(url_for("register"))


# 4 - 发送注册验证码 bp.route: 如果没有指定 method 参数，默认就是 GET 请求
@bp.route("/captcha/email", methods=["GET"])
def get_email_captcha():
    email = request.args.get("email")
    source = string.digits*6   # 6 位随机数字组合
    captcha = random.sample(source, 6)
    captcha = "".join(captcha)

    #  I/O 操作，实战中使用 其他进程执行
    message = Message(subject="注册验证码", recipients=[email],
                      body=f"您的验证码是：{captcha}")
    mail.send(message)

    # 验证码的存储 ： memcached/redis 存储；用数据库表的方式存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()

    return jsonify({"code": 200, "message": "", "data": None})


# 5 - 邮件发送测试，根据个人需求更改实际邮箱
@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["15749992333@163.com"],
                      body="123 注意查收！")
    mail.send(message)
    return "邮件发送成功"
