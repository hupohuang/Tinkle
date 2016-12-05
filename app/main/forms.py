# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField,FileField,PasswordField,ValidationError
from wtforms.validators import Required,EqualTo
from ..models import User

class XcForm(Form):
    xcname = StringField('新相册名',validators=[Required()])
    aboutxc = TextAreaField('描述')
    submit = SubmitField('确认')

class TpForm(Form):
    tppath = FileField('图片路径',validators=[Required()])
    name = StringField('图片名')
    abouttp = TextAreaField('描述')
    submit = SubmitField('确认')

class LoginForm(Form):
    username = StringField('用户名',validators=[Required()])
    password = PasswordField('密码',validators=[Required()])

class RegistrationForm(Form):
    username = StringField('用户名',validators=[Required()])
    password = PasswordField('密码',validators=[Required()])
    password2 = PasswordField('确认密码',validators=[Required(),EqualTo('password',message='密码不匹配')])
    submit = SubmitField('确认')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用')