# -*- coding: utf-8 -*-
from flask import Blueprint

main = Blueprint('main',__name__)#实例化一个Blueprint类对象创建蓝本

from . import views,errors
#导入views和errors与蓝本关联起来


