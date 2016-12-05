# -*- coding: utf-8 -*-
from flask import Blueprint

main = Blueprint('main',__name__)#实例化一个Blueprint类对象创建蓝本

from . import views,errors
#导入views和errors与蓝本关联起来
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
#把Permission类加入模板上下文，上下文管理器能让变量在所有模板中全局可访问

