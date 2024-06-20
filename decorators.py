# -- coding:utf-8 --
"""
 @Software: PyCharm
 @Date: 2024/3/1 16:14
 @Author: Glimmering
 @Function: # 装饰器
"""

from functools import wraps
from flask import g, redirect, url_for


# 保证每个页面都保持及检测登录的状态
def login_required(func):
    # 保留 func 的信息
    @wraps(func)
    # func(a,b,c)
    # func(1,2,c=3)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return inner
