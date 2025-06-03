from database import db
# class AccessDay(db.Model):
#     def __init__(self, id=None, serial=None, name=None,
#                  start_time1=None, end_time1=None,
#                  start_time2=None, end_time2=None,
#                  start_time3=None, end_time3=None,
#                  start_time4=None, end_time4=None,
#                  start_time5=None, end_time5=None):
#         self.id = id
#         self.serial = serial if serial is not None else None
#         self.name = name if name is not None else None
#         self.start_time1 = start_time1 if start_time1 is not None else None
#         self.end_time1 = end_time1 if end_time1 is not None else None
#         self.start_time2 = start_time2 if start_time2 is not None else None
#         self.end_time2 = end_time2 if end_time2 is not None else None
#         self.start_time3 = start_time3 if start_time3 is not None else None
#         self.end_time3 = end_time3 if end_time3 is not None else None
#         self.start_time4 = start_time4 if start_time4 is not None else None
#         self.end_time4 = end_time4 if end_time4 is not None else None
#         self.start_time5 = start_time5 if start_time5 is not None else None
#         self.end_time5 = end_time5 if end_time5 is not None else None
#
#     def __str__(self):
#         return f"AccessDay [id={self.id}, serial={self.serial}, name={self.name}, " \
#                f"startTime1={self.start_time1}, endTime1={self.end_time1}, " \
#                f"startTime2={self.start_time2}, endTime2={self.end_time2}, " \
#                f"startTime3={self.start_time3}, endTime3={self.end_time3}, " \
#                f"startTime4={self.start_time4}, endTime4={self.end_time4}, " \
#                f"startTime5={self.start_time5}, endTime5={self.end_time5}]"
#
#



class AccessDay(db.Model):
    __tablename__ = 'access_day'

    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String)
    name = db.Column(db.String)
    start_time1 = db.Column(db.String)
    end_time1 = db.Column(db.String)
    start_time2 = db.Column(db.String)
    end_time2 = db.Column(db.String)
    start_time3 = db.Column(db.String)
    end_time3 = db.Column(db.String)
    start_time4 = db.Column(db.String)
    end_time4 = db.Column(db.String)
    start_time5 = db.Column(db.String)
    end_time5 = db.Column(db.String)
    def __str__(self):
        return f"AccessDay [id={self.id}, serial={self.serial}, name={self.name}, " \
               f"startTime1={self.start_time1}, endTime1={self.end_time1}, " \
               f"startTime2={self.start_time2}, endTime2={self.end_time2}, " \
               f"startTime3={self.start_time3}, endTime3={self.end_time3}, " \
               f"startTime4={self.start_time4}, endTime4={self.end_time4}, " \
               f"startTime5={self.start_time5}, endTime5={self.end_time5}]"

    def to_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'name': self.name,
            'startTime1': self.start_time1,
            'endTime1': self.end_time1,
            'startTime2': self.start_time2,
            'endTime2': self.end_time2,
            'startTime3': self.start_time3,
            'endTime3': self.end_time3,
            'startTime4': self.start_time4,
            'endTime4': self.end_time4,
            'startTime5': self.start_time5,
            'endTime5': self.end_time5
        }
# 查询记录
def get_access_day_by_id(id):

    return db.session.query(AccessDay).get(id)


# 删除记录
def delete_access_day(id):

    access_day = db.session.query(AccessDay).get(id)
    if access_day:
        db.session.delete(access_day)
        db.session.commit()

    # 获取所有记录


def get_all_access_days():
    return  db.session.query(AccessDay).all()



# 插入记录
def insert_access_day(access_day):

    db.session.add(access_day)
    db.session.commit()


# 更新记录
def update_access_day(id, serial, name, start_time1, end_time1, start_time2, end_time2, start_time3, end_time3,
                      start_time4, end_time4, start_time5, end_time5):

    access_day = db.session.query(AccessDay).get(id)
    if access_day:
        access_day.serial = serial
        access_day.name = name
        access_day.start_time1 = start_time1
        access_day.end_time1 = end_time1
        access_day.start_time2 = start_time2
        access_day.end_time2 = end_time2
        access_day.start_time3 = start_time3
        access_day.end_time3 = end_time3
        access_day.start_time4 = start_time4
        access_day.end_time4 = end_time4
        access_day.start_time5 = start_time5
        access_day.end_time5 = end_time5
        db.session.commit()