# -*- coding: utf-8 -*-
from flask import render_template,redirect,url_for,request,flash,jsonify,current_app
from . import main
from ..models import User,XiangCe,TuPian
from .forms import LoginForm,XcForm,TpForm,RegistrationForm
from .. import db
from flask.ext.login import login_user,logout_user,login_required
import os,re
from PIL import Image
from werkzeug import secure_filename

def allowed_file(filename):#允许传入的文件的格式
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/')
def index():
    loginform = LoginForm()
    xclist = XiangCe.query.all()
    xcshu = len(xclist)
    tplist= []#轮播图片列表
    for i in range(xcshu):
        tp = TuPian.query.filter_by(xiangce_id=xclist[i].id).first()
        if tp is None:
            tppath = "../static/1.jpg"
            tplist.append(tppath)
            continue
        tplist.append(tp.tppath)
    return render_template('index.html',tplist=tplist,loginform=loginform,xclist=xclist)

@main.route('/register',methods=['GET','POST'])
def register():
    loginform = LoginForm()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,password=form.password.data)
        db.session.add(user)
        return redirect(url_for('.index'))
    return render_template('register.html',form=form,loginform=loginform)

@main.route('/login',methods=['GET','POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user)#在用户会话中把用户标记为已登陆
            return jsonify({'r':0})#返回json数据
        error = '用户不存在或密码错误'
        return jsonify({'r':1,'error':error})
    else:
        error = '请输入正确的用户名或密码'
        return jsonify({'r':1,'error':error})

@main.route('/logout')
def logout():
    logout_user()
    flash('你已经退出了')
    return redirect(url_for('.index'))

@main.route('/createxc',methods=['GET','POST'])
@login_required
def createxc():
    form = XcForm()
    if form.validate_on_submit():
        xiangce = XiangCe.query.filter_by(xcname=form.xcname.data).first()
        if xiangce is None:
            xiangce = XiangCe(xcname = form.xcname.data,about_xc=form.aboutxc.data,fmpath="../static/fm.jpg")
            db.session.add(xiangce)
            os.mkdir(current_app.config['UPLOAD_FOLDER']+form.xcname.data)
            os.mkdir(current_app.config['UPLOAD_FOLDER']+form.xcname.data+'/fengmian')
            os.mkdir(current_app.config['UPLOAD_FOLDER']+form.xcname.data+'/luesuo')
            #创建相册文件夹
        return redirect(url_for('.index'))
    return render_template('createxc.html', form=form)

@main.route('/managexc')
@login_required
def managexc():
    xc = XiangCe.query.all()
    tp = TuPian.query.all()
    return render_template('managexc.html',xc=xc,tp=tp)

@main.route('/xiangce/<xcname>')
def readxc(xcname):
    loginform = LoginForm()
    xc = XiangCe.query.filter_by(xcname=xcname).first()
    tp = TuPian.query.filter_by(xiangce_id=xc.id).all()
    return render_template('xiangce.html',xc=xc,tp=tp,form=form)

@main.route('/tp/<int:id>')
def tupian(id):
    tp = TuPian.query.filter_by(id=id).first()
    return render_template('tupian.html',tppath=tp.tppath)

@main.route('/edit_xc',methods=['POST'])
@login_required
def edit_xc():
    data = request.get_json('data')
    id = data['id']
    xcname = data['xcname']
    aboutxc = data['aboutxc']
    xc = XiangCe.query.filter_by(id=id).first()
    if not xc.xcname == xcname:
        xc.xcname = xcname
        xc.upgrade_xc()
    if not xc.about_xc == aboutxc:
        xc.about_xc = aboutxc
        xc.upgrade_xc()
    return jsonify({'xcname':xc.xcname,'aboutxc':xc.about_xc})


@main.route('/edit_tp',methods=['POST'])
@login_required
def edit_tp():
    data = request.get_json('data')#解析传回来的json数据，得到字典
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
    return jsonify({'r':1,'body':tp.about_tp,'tpname':tp.tpname})

@main.route('/upload/<xcname>',methods=['GET','POST'])
@login_required
def upload(xcname):
    xiangce = XiangCe.query.filter_by(xcname=xcname).first()
    form = TpForm()
    if request.method == 'GET':
        return render_template('upload.html',form=form)
    elif request.method == 'POST':
        f = form.tppath.data
        fname = secure_filename(f.filename)
        dian = fname.find('.')
        geshi = fname[dian:]
        name = form.name.data
        if name is '':#如果用户没有重命名图片则用原本的名字
            for root,dirs,files in os.walk(current_app.config['UPLOAD_FOLDER']+xcname):
            #查找同一相册文件夹内是否有同名图片
                for file in files:
                    if file == fname:
                        flash('警告')
                        return render_template('upload.html',form=form)
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER']+xcname,fname))
            name = re.match(r'([a-zA-Z0-9_]+)\.[a-zA-Z0-9]+$',fname).group(1)
        else:
            tp = TuPian.query.filter_by(xiangce_id=xiangce.id).all()
            for tp in tp:#查找同一相册数据库内是否有同名图片
                if name == tp.tpname:
                    flash('警告')
                    return render_template('upload.html',form=form)
            f.save(os.path.join(current_app.config['UPLOAD_FOLDER']+xcname,name+geshi))
        im = Image.open(current_app.config['UPLOAD_FOLDER']+xcname+'/'+name+geshi)
        im.thumbnail((600,400))#制作略缩图
        im.save(os.path.join(current_app.config['UPLOAD_FOLDER']+xcname+"/luesuo/", name+geshi))
        tp = TuPian(tppath=('../static/photo/'+xcname+'/'+name+geshi),
                    lspath = '../static/photo/'+xcname+'/luesuo/'+name+geshi,
                    about_tp=form.abouttp.data,xiangce=xiangce,tpname=name,fm=False,geshi=geshi)
        db.session.add(tp)
        xiangce.jiayi()
        if xiangce.fmpath == "../static/fm.jpg":
            w,h = im.size
            if w > h :
                box = ((w-h)/2,0,(w-h)/2+h,h)
                nim = im.crop(box)
            if h > w :
                box = (0,(h-w)/2,w,(h-w)/2+w)
                nim = im.crop(box)
            nim.thumbnail((200,200))#裁剪图片
            nim.save(os.path.join(current_app.config['UPLOAD_FOLDER']+xcname+"/fengmian/", name+geshi))
            xiangce.fmpath = '../static/photo/'+xcname+'/fengmian/'+name+geshi
            db.session.add(xiangce)
            tp.fm = True
            db.session.add(tp)
        xiangce.upgrade_xc()
        return redirect(url_for('.readxc',xcname=xcname))

@main.route('/edit_fm',methods=['POST'])
def edit_fm():
    data = request.get_json('data')
    id = data['id']
    tp = TuPian.query.filter_by(id=id).first()
    xc = XiangCe.query.filter_by(id=tp.xiangce_id).first()
    xc.edit_fm(id)
    return jsonify({'r':1})

@main.route('/delete-tp/<int:id>')
@login_required
def delete_tp(id):
    tp = TuPian.query.get_or_404(id)
    xc = XiangCe.query.filter_by(id=tp.xiangce_id).first()
    tp.delete_tp()
    return (''),204

@main.route('/delete-xc/<int:id>')
@login_required
def delete_xc(id):
    xc = XiangCe.query.get_or_404(id)
    xc.delete_xc()
    return (''),204
