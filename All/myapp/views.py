from flask import Blueprint,render_template,jsonify,json,request,redirect,make_response,url_for
from .models import Data,User
from . import db
import pymysql
import json
blue = Blueprint('user',__name__)


#登陆
@blue.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html',context=None)
    name=request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.phone_number==name).first()
    if not user:
        return render_template('login.html',message='账户不存在')
    else:
        if not user.password==password:
            return render_template('login.html', message='密码不正确')
    resp = make_response(redirect('index'))
    resp.set_cookie('u_id', str(user.id))
    return resp

#
#注册
@blue.route('/regiest', methods=['GET', 'POST'])
def regiest():
    if request.method=='GET':
        return render_template('regiest.html',context=None)
    phone=request.form.get('phone')
    name=request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter(User.phone_number==phone).first()

    if user:

        return render_template('regiest.html',message='该手机号已经被注册')
    else:
        if not all([phone,name,password]):
            content = {
                'message': '请填写所有信息',
            }
            return render_template('regiest.html', message='请填写所有信息')
        u=User()
        u.name=name
        u.phone_number=phone
        u.password=password
        u.user_type=1
        db.session.add(u)
        db.session.commit()

        return render_template('regiest.html', message='注册成功!')
    return render_template('regiest.html')
#
#退出登陆
@blue.route('/login_out', methods=['GET', 'POST'])
def login_out():
    return redirect('/user/login')
#
#首页
def function(date):
    return date['value']

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
def get_dic():
    db = pymysql.connect("localhost", "root", "test123", "douban1")

    cursor = db.cursor()

    cursor.execute("SELECT * from data")

    data = cursor.fetchall()
    name, juqing, shijian, score, pl, mv_time, guojia = [], [], [], [], [], [], []
    for item in data:
        name.append(item[0])
        juqing.append(item[3])
        shijian.append(item[-4])
        try:
            score.append(float(item[-2]))
        except Exception as e:
            score.append(8.0)
        try:
            pl.append(int(item[-1]))
        except Exception as e:
            pl.append(10000)

        mv_time.append(int(item[-3]))
        guojia.append(item[-6])

    res_dict = {'name': name, 'juqing': juqing, 'shijian': shijian, 'score': score, 'pl': pl, 'mv_time': mv_time,
                'guojia': guojia}
    res_dict_df = pd.DataFrame(res_dict)

    # 关闭数据库连接
    db.close()

    # 图2   test123
    t2 = []

    s = res_dict_df.groupby(guojia).count()['guojia']

    for item in dict(s).keys():
        d = {}
        d['value'] = dict(s)[item]
        d['name'] = item
        t2.append(d)
    t2.sort(key=function, reverse=True)
    # print(t2)

    # 图3 各个类型电影数量  t3

    t3 = []
    s = res_dict_df.groupby(juqing).count()['juqing']
    for item in dict(s).keys():
        d = {}
        d['value'] = dict(s)[item]
        d['name'] = item
        t3.append(d)
    t3.sort(key=function, reverse=True)
    # print(t3)

    # 图4 2000-2020电影趋势  r

    s = res_dict_df.groupby(shijian).count()['shijian']
    r = {}
    for item in dict(s).keys():
        try:
            ww=int(item)
        except:
            ww=1999
        if ww >= 2000:
            r[item] = dict(s)[item]

    # print(r)

    # 图5 分段统计  t5
    def cut_to(x):

        if x <= 5:
            return '0-5'
        elif x >= 5 and x < 6:
            return '5~6'
        elif x >= 6 and x < 7:
            return '6~7'
        elif x >= 7 and x < 8:
            return '7~8'
        elif x >= 8 and x < 9:
            return '8~9'
        elif x >= 9 and x < 10:
            return '9~10'

    res_dict_df['fenduan'] = res_dict_df['score'].map(cut_to)
    s = res_dict_df.groupby('fenduan').count()['juqing']

    t5 = []
    for item in dict(s).keys():
        d = {}
        d['value'] = dict(s)[item]
        d['name'] = item
        t5.append(d)

    # print(t5)

    # 图6  pl, f_name

    s = res_dict_df.sort_values(by='pl', ascending=False)['name'].tolist()
    pl = sorted(res_dict_df['pl'].tolist(), reverse=True)[:10]
    f_name = s[:10]

    # 图7  t7

    def cut_to1(x):

        if x < 90:
            return '0~90分'
        elif x >= 90 and x < 100:
            return '90~100分'
        elif x >= 100 and x < 110:
            return '100~110分'
        elif x >= 110 and x < 120:
            return '110~120分'
        elif x >= 120 and x < 130:
            return '120~130分'
        elif x >= 130:
            return '130+分'

    res_dict_df['fenduan'] = res_dict_df['mv_time'].map(cut_to1)
    s = res_dict_df.groupby('fenduan').count()['juqing']

    t7 = []
    for item in dict(s).keys():
        d = {}
        d['value'] = dict(s)[item]
        d['name'] = item
        t7.append(d)

    res_d = {}
    res_d['t2'] = t2[:11]
    res_d['t3'] = t3
    res_d['t4'] = r
    res_d['t5'] = t5
    res_d['t6_1'] = pl
    res_d['t6_2'] = f_name
    res_d['t7'] = t7
    return res_d
#返回数据
import pandas as pd
import numpy as np
@blue.route('/get_data', methods=['GET', 'POST'])
def get_data():
    data=json.loads(json.dumps(get_dic(), cls=NpEncoder))
    return data
#显示可视化界面
@blue.route('/index', methods=['GET', 'POST'])
def index():
    u_id = request.cookies.get('u_id')
    user = User.query.filter(User.id == u_id).first()
    return render_template('echarts.html',user=user)

#显示用户管理
@blue.route('/user_manager', methods=['GET', 'POST'])
def user_manager():
    u = request.cookies.get('u_id')
    keywords=request.args.get('keywords')
    u_id=request.cookies.get('u_id')
    stu=User.query.filter(User.id==u_id).first()
    scores=User.query.filter(User.id!=u).all()
    if keywords:
        scores = User.query.filter(User.name==keywords).filter(User.id!=u).all()
        return render_template('user_manager.html', data={'stu': stu, 'scores': scores})
    return render_template('user_manager.html',data={'stu':stu,'scores':scores})


#编辑用户
@blue.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    u_id1=request.cookies.get("u_id")
    user1 = User.query.filter(User.id == u_id1).first()
    if request.method=='GET':
        u_id = request.args.get('u_id')
        user = User.query.filter(User.id == u_id).first()
        return render_template('edit_user.html',data={'user':user,"message":None,'user1':user1})
    user_id=request.form.get('user_id')
    nick_name=request.form.get('nick_name')

    password=request.form.get('password')
    user = User.query.filter(User.id == user_id).first()
    user.name=nick_name
    user.password=password
    db.session.add(user)
    db.session.commit()
    return redirect('user_manager')
#删除用户
@blue.route('/admin_delete', methods=['GET', 'POST'])
def admin_delete():
    u_id=request.args.get('u_id')
    user=User.query.filter(User.id==u_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('user_manager')

#修改密码
@blue.route('/reset_pwd', methods=['GET', 'POST'])
def admin_upreset_pwddate():
    u_id = request.cookies.get('u_id')
    score=User.query.filter(User.id==u_id).first()
    if request.method=='GET':
        return render_template('info_edit.html',data={'score':score,'message':None})
    phone=request.form.get('phone_number')
    password=request.form.get('password')
    score.phone_number=phone
    score.password=password
    db.session.add(score)
    db.session.commit()
    return render_template('info_edit.html', data={'score':score,'message':'修改成功！'})