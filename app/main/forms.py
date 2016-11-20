# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField,BooleanField,FileField,PasswordField
from wtforms.validators import Required

class XcForm(Form):
    xcname = StringField('新相册名',validators=[Required()])
    submit = SubmitField('确认')

class TpForm(Form):
    tppath = FileField('图片路径',validators=[Required()])
    name = StringField('图片名')
    submit = SubmitField('确认')

class LoginForm(Form):
    username = StringField('用户名',validators=[Required()])
    password = PasswordField('密码',validators=[Required()])

class EditTp(Form):
    body = TextAreaField('body')