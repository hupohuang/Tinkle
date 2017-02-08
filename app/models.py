# -*- coding: utf-8 -*-
from . import db,login_manager
from flask.ext.login import UserMixin,AnonymousUserMixin
from flask import current_app
from datetime import datetime
import os,shutil
from PIL import Image

@login_manager.user_loader
def load_user(user_id):#Flask_Login要求程序实现的回调函数，使用指定的标识符加载用户
    return User.query.get(int(user_id))

class Permission:
    USER = 0x07
    ADMINISTER = 0xff

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.USER, True),
            'Administrator': (Permission.ADMINISTER, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(),default=datetime.now)
    last_seen = db.Column(db.DateTime(),default=datetime.now)
    xiangces = db.relationship('XiangCe',backref='user',lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.username == current_app.config['TINKLE_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def verify_password(self,password):#密码认证
        if self.password == password:
            return True

    def can(self,permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

class AnonymouseUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymouseUser

class XiangCe(db.Model):
    __tablename__ = 'xiangces'
    id = db.Column(db.Integer,primary_key=True)
    xcname = db.Column(db.String(64),unique=True)
    tpshu = db.Column(db.Integer,default=0)
    about_xc = db.Column(db.Text())
    fmpath = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(),default=datetime.now)
    last_seen = db.Column(db.DateTime(),default=datetime.now)
    tupians = db.relationship('TuPian',backref='xiangce',lazy='dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def jiayi(self):#图片数量+1
        self.tpshu = self.tpshu + 1
        db.session.add(self)

    def jianyi(self):#图片数量-1
        self.tpshu = self.tpshu - 1
        db.session.add(self)

    def edit_fm(self,id):
        tp = TuPian.query.filter_by(id=id).first()
        xc = XiangCe.query.filter_by(id=tp.xiangce_id).first()
        oldfm = TuPian.query.filter_by(xiangce_id=xc.id).filter_by(fm=True).first()
        os.remove(current_app.config['UPLOAD_FOLDER']+xc.fmpath[16:])
        oldfm.fm = False
        tp.fm = True
        db.session.add(oldfm,tp)
        im = Image.open(current_app.config['UPLOAD_FOLDER']+tp.tppath[16:])
        w,h = im.size
        if w > h :
            box = ((w-h)/2,0,(w-h)/2+h,h)
            nim = im.crop(box)
        if h > w :
            box = (0,(h-w)/2,w,(h-w)/2+w)
            nim = im.crop(box)
        nim.thumbnail((200,200))#裁剪图片
        nim.save(os.path.join(current_app.config['UPLOAD_FOLDER']+xc.xcname+"/fengmian/", tp.tpname+tp.geshi))
        xc.fmpath = '../static/photo/'+xc.xcname+'/fengmian/'+tp.tpname+tp.geshi
        db.session.add(xc)

    def upgrade_xc(self):#相册改动时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def delete_xc(self):
        tp = TuPian.query.filter_by(xiangce_id=self.id).all()
        if tp == '':
            os.remove(current_app.config['UPLOAD_FOLDER'][:19]+self.fmpath[2:])
        else:
            for tp in tp:
                os.remove(current_app.config['UPLOAD_FOLDER']+tp.tppath[16:])
                os.remove(current_app.config['UPLOAD_FOLDER']+tp.lspath[16:])
                db.session.delete(tp)
        shutil.rmtree(current_app.config['UPLOAD_FOLDER']+self.xcname)
        db.session.delete(self)

class TuPian(db.Model):
    __tablename__ = 'tupians'
    id = db.Column(db.Integer,primary_key=True)
    fm = db.Column(db.Boolean)
    tppath = db.Column(db.String(128),unique=True)
    lspath = db.Column(db.String(128),unique=True)
    tpname = db.Column(db.String(64))
    about_tp = db.Column(db.Text())
    geshi = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime(),default=datetime.now)
    last_since = db.Column(db.DateTime(),default=datetime.now)
    xiangce_id = db.Column(db.Integer,db.ForeignKey('xiangces.id'))

    def upgrade_tp(self):#图片改动时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def delete_tp(self):
        xc = XiangCe.query.filter_by(id=self.xiangce_id).first()
        os.remove(current_app.config['UPLOAD_FOLDER']+self.tppath[16:])
        os.remove(current_app.config['UPLOAD_FOLDER']+self.lspath[16:])
        if self.fm == True:
            tp = TuPian.query.filter_by(xiangce_id=xc.id).filter_by(fm=False).first()
            if tp is None:
                xc.fmpath = "../static/fm.jpg"
            else:
                xc.edit_fm(tp.id)
        db.session.delete(self)
        xc.jianyi()
        xc.upgrade_xc()
