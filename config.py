# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'hard to guess string'
    UPLOAD_FOLDER = 'f:/ceshi/Tinkle/app/static/photo/'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True#每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/test'
    #SQLALCHEMY连接mysql数据库

config = {
    'development':DevelopmentConfig,

    'default':DevelopmentConfig
}
