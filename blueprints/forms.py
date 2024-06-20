# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/3/2 11:53
 @Author: Glimmering
 @Function: 系统注册与登录中的表单提交
"""

import wtforms
from models import UserModel, EmailCaptchaModel
from exts import db
from wtforms.validators import Email, Length, EqualTo, InputRequired

# form: 主要用来验证前端提交的注册数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=6, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证 1.邮箱是否已被注册，2.验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")

        # 自定义脚本，定期删除
        # else:  # todo 可以删除该验证码
        #     db.session.delete(captcha_model)
        #     db.session.commit()


# 登录表单验证
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])


# 发布问题表单验证
class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=1, max=30, message="标题格式错误")])
    content = wtforms.StringField(validators=[Length(min=1, message="内容格式错误")])

# 发布回答表单验证
class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message="内容格式错误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id！")])