from . import db
import datetime
class Data(db.Model):
    __tablename__ = "data"
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)

    name=db.Column(db.String(50), nullable=False)
    daoyan = db.Column(db.String(50), nullable=False)
    zhuyan = db.Column(db.String(100), nullable=False)
    juqing = db.Column(db.String(50), nullable=False)
    diqu = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    shijian = db.Column(db.String(50), nullable=False)
    score = db.Column(db.String(50), nullable=False)

    pl = db.Column(db.String(50), nullable=False)




class User(db.Model):

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(50), nullable=False)
    phone_number=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(50), nullable=False)
    user_type=db.Column(db.Integer)
    img=db.Column(db.String(100))








