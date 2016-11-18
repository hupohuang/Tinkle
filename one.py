# -*- coding: utf-8 -*-
import os,re,shutil
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template,redirect,url_for,session,abort,request,flash,jsonify
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField,PasswordField,FileField,TextAreaField
from wtforms.validators import Required
from flask.ext.migrate import Migrate,MigrateCommand
from werkzeug import secure_filename
from flask.ext.login import login_user,UserMixin,LoginManager,logout_user,login_required,current_user
from datetime import datetime
from PIL import Image

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['UPLOAD_FOLDER'] = 'f:/ceshi/Tinkle/static/photo/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(128))

    def verify_password(self,password):
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

    def jiayi(self):
        self.tpshu = XiangCe.tpshu + 1
        db.session.add(self)

    def jianyi(self):
        self.tpshu = XiangCe.tpshu - 1
        db.session.add(self)

    def upgrade_xc(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def delete_xc(self):
        tp = TuPian.query.filter_by(xiangce_id=self.id).all()
        if tp is not None:
            for tp in tp:
                os.remove(app.config['UPLOAD_FOLDER']+tp.tppath[16:])
                os.remove(app.config['UPLOAD_FOLDER']+tp.fmpath[16:])
                os.remove(app.config['UPLOAD_FOLDER']+tp.lspath[16:])
                db.session.delete(tp)
        shutil.rmtree(app.config['UPLOAD_FOLDER']+self.xcname)
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


    def upgrade_tp(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def delete_tp(self):
        xc = XiangCe.query.filter_by(id=self.xiangce_id).first()
        os.remove(app.config['UPLOAD_FOLDER']+self.tppath[16:])
        os.remove(app.config['UPLOAD_FOLDER']+self.fmpath[16:])
        os.remove(app.config['UPLOAD_FOLDER']+self.lspath[16:])
        db.session.delete(self)
        xc.jianyi()
        xc.upgrade_xc()

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    form = LoginForm()
    xclist = XiangCe.query.all()
    xcshu = len(xclist)
    fmlist = []
    tplist= []
    for i in range(xcshu):
        tp = TuPian.query.filter_by(xiangce_id=xclist[i].id).first()
        if tp is None:
            tppath = "../static/1.jpg"
            tplist.append(tppath)
            fmlist.append((xclist[i].xcname,"../static/fm.jpg"))
            continue
        tplist.append(tp.tppath)
        fmlist.append((xclist[i].xcname,tp.fmpath))
    return render_template('index.html',xclist=xclist,tplist=tplist,form=form,fmlist=fmlist)
    #return render_template('ceshi.html')

@app.route('/login',methods=['GOT','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return jsonify({'r':0})
        error = '用户不存在或密码错误'
        return jsonify({'r':1,'error':error})
    else:
        error = '请输入正确的用户名或密码'
        return jsonify({'r':1,'error':error})

@app.route('/logout')
def logout():
    logout_user()
    flash('你已经退出了')
    return redirect(url_for('index'))

@app.route('/createxc',methods=['GET','POST'])
@login_required
def createxc():
    form = XcForm()
    if form.validate_on_submit():
        xiangce = XiangCe.query.filter_by(xcname=form.xcname.data).first()
        if xiangce is None:
            xiangce = XiangCe(xcname = form.xcname.data)
            db.session.add(xiangce)
            os.mkdir(app.config['UPLOAD_FOLDER']+form.xcname.data)
            os.mkdir(app.config['UPLOAD_FOLDER']+form.xcname.data+'/fengmian')
            os.mkdir(app.config['UPLOAD_FOLDER']+form.xcname.data+'/luesuo')
        return redirect(url_for('index'))
    return render_template('createxc.html', form=form)

@app.route('/managexc')
@login_required
def managexc():
    xc = XiangCe.query.all()
    tp = TuPian.query.all()
    return render_template('managexc.html',xc=xc,tp=tp)

@app.route('/xiangce/<xcname>')
def readxc(xcname):
    form = LoginForm()
    xc = XiangCe.query.filter_by(xcname=xcname).first()
    tp = TuPian.query.filter_by(xiangce_id=xc.id).all()
    return render_template('xiangce.html',xc=xc,tp=tp,form=form)

@app.route('/edit_tp',methods=['POST'])
@login_required
def edit_tp():
    data = request.get_json('data')
    id = data['id']
    body = data['body']
    name = data['tpname']
    tp = TuPian.query.filter_by(id=id).first()
    if not tp.about_tp == body:
        tp.about_tp = body
        tp.upgrade_tp()
    if not tp.tpname == name:
        tp.tpname = name
        tp.upgrade_tp()
    return jsonify({'r':1,'body':body,'tpname':name})

@app.route('/upload/<xcname>',methods=['GET','POST'])
@login_required
def upload(xcname):
    xiangce = XiangCe.query.filter_by(xcname=xcname).first()
    form = TpForm()
    if request.method == 'GET':
        return render_template('upload.html',form=form)
    elif request.method == 'POST':
        f = form.tppath.data
        fname = secure_filename(f.filename)
        for root,dirs,files in os.walk(app.config['UPLOAD_FOLDER']+xcname):
            for file in files:
                if file == fname:
                    flash('警告')
                    return render_template('upload.html',form=form)
        f.save(os.path.join(app.config['UPLOAD_FOLDER']+xcname, fname))
        dian = fname.find('.')
        houxu = fname[dian:]
        name = form.name.data
        if name is '':
            name = re.match(r'([a-zA-Z0-9_]+)\.[a-zA-Z0-9]+$',fname).group(1)
        else:
            os.rename(app.config['UPLOAD_FOLDER']+xcname+'/'+fname,app.config['UPLOAD_FOLDER']+xcname+'/'+name+houxu)

        im = Image.open(app.config['UPLOAD_FOLDER']+xcname+'/'+name+houxu)
        im.thumbnail((600,400))
        im.save(os.path.join(app.config['UPLOAD_FOLDER']+xcname+"/luesuo/", name+houxu))
        w,h = im.size
        if w > h :
            box = ((w-h)/2,0,(w-h)/2+h,h)
            nim = im.crop(box)
        if h > w :
            box = (0,(h-w)/2,w,(h-w)/2+w)
            nim = im.crop(box)
        nim.thumbnail((200,200))
        nim.save(os.path.join(app.config['UPLOAD_FOLDER']+xcname+"/fengmian/", name+houxu))
        tp = TuPian(tppath=('../static/photo/'+xcname+'/'+name+houxu),
                    fmpath = '../static/photo/'+xcname+'/fengmian/'+name+houxu,
                    lspath = '../static/photo/'+xcname+'/luesuo/'+name+houxu,xiangce=xiangce,tpname=name)
        db.session.add(tp)
        xiangce.jiayi()
        xiangce.upgrade_xc()
        return redirect(url_for('readxc',xcname=xcname))

@app.route('/delete-tp/<int:id>')
@login_required
def delete_tp(id):
    tp = TuPian.query.get_or_404(id)
    xc = XiangCe.query.filter_by(id=tp.xiangce_id).first()
    tp.delete_tp()
    flash('图片已删除')
    return redirect(url_for('readxc',xcname=xc.xcname))

@app.route('/delete-xc/<int:id>')
@login_required
def delete_xc(id):
    xc = XiangCe.query.get_or_404(id)
    xc.delete_xc()
    flash('相册已删除')
    return redirect(url_for('managexc'))

if __name__ == '__main__':
    app.run(debug=True)
