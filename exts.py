# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/3/1 16:14
 @Author: Glimmering
 @Function: 解决循环引用的问题
"""

# flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
