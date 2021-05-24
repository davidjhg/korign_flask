from flask import Flask, render_template

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask import request
from models import db
# import config

app = Flask(__name__)

import os

# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')

# SQLAlchemy 설정

# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()
migrate = Migrate(app, db)

from models import User,SignUser
import json 
# @app.route('/')
# def index():
#     user_list = User.query.all()

#     return render_template('index_prev.html',user_list=user_list)
    
jaeum_prev2cur = {
    'g':'n','n':'d','d':'r','r':'m','m':'b','b':'s','s':'ng',
    'ng':'j','j':'ch','ch':'k','k':'t','t':'p','p':'h'
}
moeum_prev2cur = {
    'a':'ya'
}

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/index')
def index():
    username = request.args.get('username')
    print('[DEBUG] username',username)
    option2ref = {
        '자음연습':'g',
        '모음연습':'a'
    }
    return render_template('index.html',option2ref = option2ref,username=username)

@app.route('/korign/<string:ref>/<string:username>')
def korign(ref,username):
    print('ref',ref)
    sec = request.args.get('sec',0)
    print(sec,type(sec))
    print(username,type(username))
    
    if ref == 'fin':
        print("[DEBUG] fin")
        return render_template('login.html',sec=sec)

    if ref in jaeum_prev2cur.keys():
        image_file = 'dataset/ja-eum/pic/%s.png'%(ref)
        f = open('./static/dataset/ja-eum/%s.json'%(ref))
        data_json = json.load(f)
        f.close()
    elif ref in moeum_prev2cur.keys():
        image_file = 'dataset/mo-eum/pic/%s.png'%(ref)
        f = open('./static/dataset/mo-eum/%s.json'%(ref))
        data_json = json.load(f)
        f.close()

    return render_template('korign.html',data_json = data_json,image_file=image_file,cur=ref,sec=sec,username=username)

    print('ref',ref)
    if ref == 'g' or ref == 'a': # new start 
        if ref in jaeum_prev2cur.keys():
            image_file = 'dataset/ja-eum/pic/%s.png'%(ref)
            f = open('./static/dataset/ja-eum/%s.json'%(ref))
            data_json = json.load(f)
            f.close()
        elif ref in moeum_prev2cur.keys():
            image_file = 'dataset/mo-eum/pic/%s.png'%(ref)
            f = open('./static/dataset/mo-eum/%s.json'%(ref))
            data_json = json.load(f)
            f.close()
    elif ref == 'h' or ref == 'i':
        pass 
    else:
        if ref in jaeum_prev2cur.keys():
            cur = jaeum_prev2cur[ref]
            image_file = 'dataset/ja-eum/pic/%s.png'%(ref)
            f = open('./static/dataset/ja-eum/%s.json'%(ref))
            data_json = json.load(f)
            f.close()
        elif ref in moeum_prev2cur.keys():
            cur = moeum_prev2cur[ref]
            image_file = 'dataset/mo-eum/pic/%s.png'%(ref)
            f = open('./static/dataset/mo-eum/%s.json'%(ref))
            data_json = json.load(f)
            f.close()

    return render_template('korign.html',data_json = data_json,image_file=image_file,cur=cur)

    if ref == 0: # 자음연습
        f = open('./static/dataset/ja-eum/k.json')
        data_json = json.load(f)
        f.close()
        
    elif ref == 1:
        f = open('./static/dataset/ja-eum/k.json')
        data_json = json.load(f)
        f.close()
    
    return render_template('korign.html',data_json = data_json,image_file="dataset/ja-eum/pic/k.png")

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/sign_detail')
def sign_detail():
    users = SignUser.query.all()

    return render_template('sign_detail.html')



@app.route('/login_check')
def login_check():
    username = request.args.get('username')
    print('[DEBUG] username',username)
  
    return render_template('index.html', username=username) 

@app.route('/detail/<int:id>/')
def user_detail(id):
    print('id:',id)
    user = User.query.get_or_404(id)
    return render_template('detail.html', user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

