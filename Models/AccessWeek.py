from database import db
class AccessWeek:
    def __init__(self, id=None, serial=None, name=None,
                 monday=None, tuesday=None,
                 wednesday=None, thursday=None,
                 friday=None, saturday=None,
                 sunday=None):
        self.id = id
        self.serial = serial if serial is not None else None
        self.name = name if name is not None else None
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday

    def __str__(self):
        return f"AccessWeek [id={self.id}, serial={self.serial}, name={self.name}, " \
               f"monday={self.monday}, tuesday={self.tuesday}, " \
               f"wednesday={self.wednesday}, thursday={self.thursday}, " \
               f"friday={self.friday}, saturday={self.saturday}, " \
               f"sunday={self.sunday}]"


# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# engine = create_engine('sqlite:///database.db')
# Session = sessionmaker(bind=engine)
# Base = declarative_base()


class AccessWeek(db.Model):
    __tablename__ = 'access_week'

    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String)
    name = db.Column(db.String)
    monday = db.Column(db.Integer)
    tuesday = db.Column(db.Integer)
    wednesday = db.Column(db.Integer)
    thursday = db.Column(db.Integer)
    friday = db.Column(db.Integer)
    saturday = db.Column(db.Integer)
    sunday = db.Column(db.Integer)


# 查询记录
def get_access_week_by_id(id):

    return db.session.query(AccessWeek).get(id)


# 删除记录
def delete_access_week(id):

    access_week = db.session.query(AccessWeek).get(id)
    if access_week:
        db.session.delete(access_week)
        db.session.commit()

    # 获取所有记录


def get_all_access_weeks():

    return db.session.query(AccessWeek).all()


# 插入记录
def insert_access_week(access_week):

    db.session.add(access_week)
    db.session.commit()


# 更新记录
def update_access_week(id, serial, name, monday, tuesday, wednesday, thursday, friday, saturday, sunday):

    access_week = db.session.query(AccessWeek).get(id)
    if access_week:
        access_week.serial = serial
        access_week.name = name
        access_week.monday = monday
        access_week.tuesday = tuesday
        access_week.wednesday = wednesday
        access_week.thursday = thursday
        access_week.friday = friday
        access_week.saturday = saturday
        access_week.sunday = sunday
        db.session.commit()