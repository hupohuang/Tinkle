# -*- coding: utf-8 -*-
import os
from app import create_app,db
from app.models import User,XiangCe,TuPian
from flask.ext.script import Manager,Shell
from flask.ext.migrate import Migrate,MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():#注册程序、数据库实例、模型，这些对象直接导入shell
    return dict(app=app,db=db,User=User,
                XiangCe=XiangCe,TuPian=TuPian)

manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)#导出数据库迁移命令

if __name__ == '__main__':
    app.run()