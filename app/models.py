# -*- coding: utf-8 -*-
from . import db,login_manager
from flask.ext.login import UserMixin
from flask import current_app
from datetime import datetime
import os,shutil

@login_manager.user_loader
def load_user(user_id):#Flask_Login要求程序实现的回调函数，使用指定的标识符加载用户
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(128))

    def verify_password(self,password):#密码认证
        if self.password == password:
            return True

class XiangCe(db.Model):
    __tablename__ = 'xiangces'
    id = db.Column(db.Integer,primary_key=True)
    xcname = db.Column(db.String(64),unique=True)
    tpshu = db.Column(db.Integer,default=0)
    about_xc = db.Column(db.Text())
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)
    tupians = db.relationship('TuPian',backref='xiangce',lazy='dynamic')

    def jiayi(self):#图片数量+1
        self.tpshu = XiangCe.tpshu + 1
        db.session.add(self)

    def jianyi(self):#图片数量-1
        self.tpshu = XiangCe.tpshu - 1
        db.session.add(self)

    def upgrade_xc(self):#相册改动时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def delete_xc(self):
        tp = TuPian.query.filter_by(xiangce_id=self.id).all()
        if tp is not None:
            for tp in tp:
                os.remove(current_app.config['UPLOAD_FOLDER']+tp.tppath[16:])
                os.remove(current_app.config['UPLOAD_FOLDER']+tp.fmpath[16:])
                os.remove(current_app.config['UPLOAD_FOLDER']+tp.lspath[16:])
                db.session.delete(tp)
        shutil.rmtree(current_app.config['UPLOAD_FOLDER']+self.xcname)
        db.session.delete(self)

class TuPian(db.Model):
    __tablename__ = 'tupians'
    id = db.Column(db.Integer,primary_key=True)
    tppath = db.Column(db.String(128),unique=True)
    fmpath = db.Column(db.String(128),unique=True)
    lspath = db.Column(db.String(128),unique=True)
    tpname = db.Column(db.String(64))
    about_tp = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(),default=datetime.utcnow)
    last_since = db.Column(db.DateTime(),default=datetime.utcnow)
    xiangce_id = db.Column(db.Integer,db.ForeignKey('xiangces.id'))


    def upgrade_tp(self):#图片改动时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def delete_tp(self):
        xc = XiangCe.query.filter_by(id=self.xiangce_id).first()
        os.remove(current_app.config['UPLOAD_FOLDER']+self.tppath[16:])
        os.remove(current_app.config['UPLOAD_FOLDER']+self.fmpath[16:])
        os.remove(current_app.config['UPLOAD_FOLDER']+self.lspath[16:])
        db.session.delete(self)
        xc.jianyi()
        xc.upgrade_xc()
