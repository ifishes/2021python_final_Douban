from flask import  Flask
from myapp.views import blue
import os
import pandas as pd
import pymysql
from myapp import db
def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    app=Flask(__name__,static_folder=static_dir,template_folder=templates_dir)
    app.register_blueprint(blueprint=blue,url_prefix='/user')
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:123456@127.0.0.1:3306/douban1'
    app.config['DEBUG']=True
    app.config['SECRET_KEY'] = '123456'
    db.init_app(app)
    return app
BASE_DIR = os.path.dirname(__file__)



def function(date):
    return date['value']


def get_dic():
    db = pymysql.connect("localhost", "root", "test123", "douban")

    cursor = db.cursor()

    cursor.execute("SELECT * from data")

    data = cursor.fetchall()
    name, juqing, shijian, score, pl, mv_time, guojia = [], [], [], [], [], [], []
    for item in data:
        name.append(item[0])
        juqing.append(item[3])
        shijian.append(item[-4].split('-')[0])
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
        if int(item) >= 2000:
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
            return '0-90'
        elif x >= 90 and x < 100:
            return '90~100'
        elif x >= 100 and x < 110:
            return '100~110'
        elif x >= 110 and x < 120:
            return '110~120'
        elif x >= 120 and x < 130:
            return '120~130'
        elif x >= 130:
            return '130+'

    res_dict_df['fenduan'] = res_dict_df['mv_time'].map(cut_to1)
    s = res_dict_df.groupby('fenduan').count()['juqing']

    t7 = []
    for item in dict(s).keys():
        d = {}
        d['value'] = dict(s)[item]
        d['name'] = item
        t7.append(d)

    res_d = {}
    res_d['t2'] = t2[:5]
    res_d['t3'] = t3
    res_d['t4'] = r
    res_d['t5'] = t5
    res_d['t6_1'] = pl
    res_d['t6_2'] = f_name
    res_d['t7'] = t7

    return res_d