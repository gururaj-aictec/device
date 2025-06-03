# class EnrollInfo:
#     def __init__(self, id=None, enroll_id=None, backupnum=None, imagepath=None, signatures=None):
#         self.id = id
#         self.enroll_id = enroll_id
#         self.backupnum = backupnum
#         self.imagepath = imagepath
#         self.signatures = signatures if signatures is not None else None
#
#     def __str__(self):
#         return f"EnrollInfo [id={self.id}, enrollId={self.enroll_id}, backupnum={self.backupnum}, imagePath={self.imagepath}, signatures={self.signatures}]"
from database import db
#
# from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# engine = create_engine('sqlite:///database.db')
# Session = sessionmaker(bind=engine)
# Base = declarative_base()


class EnrollInfo(db.Model):
    __tablename__ = 'enrollinfo'

    id = db.Column(db.Integer, primary_key=True)
    enroll_id = db.Column(db.Integer)
    backupnum = db.Column(db.Integer)
    imagepath = db.Column(db.String)
    signatures = db.Column(db.Text)

    def __str__(self):
        return "EnrollInfo [id={}, enroll_id={}, backupnum={}, imagepath={}, signatures={}]".format(self.id,
                                                                                                    self.enroll_id,
                                                                                                    self.backupnum,
                                                                                                    self.imagepath,
                                                                                                    self.signatures)

    def to_dict(self):
        return {
            "id": self.id,
            "enroll_id": self.enroll_id,
            "backupnum": self.backupnum,
            "imagepath": self.imagepath,
            "signatures": self.signatures
        }
    # 插入新的记录
    def insert_enroll_info(self,**info):
        info = EnrollInfo(**info)

        db.session.add(info)
        db.session.commit()

    # 查询所有记录
    # def get_all_enroll_info():
    #     session = db.Session()
    #     return session.query(EnrollInfo).all()
    def get_all_enroll_info(self):
        return EnrollInfo.query.all()
    def select_all(self):
        return EnrollInfo.query.all()
    # 根据主键查询记录
    def get_enroll_info_by_id(self,id):

        return db.session.query(EnrollInfo).get(id)

    # 根据enroll_id查询记录
    def get_enroll_info_by_enroll_id(self,enroll_id):

        return db.session.query(EnrollInfo).filter_by(enroll_id=enroll_id).first()

    def selectByBackupnum(self, enroll_id , backupnum):

        return db.session.query(EnrollInfo).filter_by(enroll_id=enroll_id, backupnum=backupnum).first()
    # 更新记录
    def update_enroll_info(self,id, enroll_id, backupnum, imagepath, signatures):

        info = db.session.query(EnrollInfo).get(id)
        if info:
            info.enroll_id = enroll_id
            info.backupnum = backupnum
            info.imagepath = imagepath
            info.signatures = signatures
            db.session.commit()

    def delete_enroll_info(self,id):

        info = db.session.query(EnrollInfo).get(id)
        if info:
            db.session.delete(info)
            db.session.commit()
    def delete_by_enroll_id(self,id):

        info = db.session.query(EnrollInfo).get(id)
        if info:
            db.session.delete(info)
            db.session.commit()

# def insert_enroll_info(enroll_id, backupnum, imagepath, signatures):
#     info = EnrollInfo(enroll_id=enroll_id, backupnum=backupnum, imagepath=imagepath, signatures=signatures)

#     db.ession.add(info)
#     db.ession.commit()
def insert_enroll_info(**info):
    info = EnrollInfo(**info)

    db.session.add(info)
    db.session.commit()


# 查询所有记录
# def get_all_enroll_info():
#     session = db.Session()
#     return session.query(EnrollInfo).all()
def get_all_enroll_info():
    return EnrollInfo.query.all()

# 根据主键查询记录
def get_enroll_info_by_id(id):

    return db.session.query(EnrollInfo).get(id)


# 根据enroll_id查询记录
def get_enroll_info_by_enroll_id(enroll_id):

    return db.session.query(EnrollInfo).filter_by(enroll_id=enroll_id).first()


# 更新记录
def update_enroll_info(id, enroll_id, backupnum, imagepath, signatures):

    info = db.session.query(EnrollInfo).get(id)
    if info:
        info.enroll_id = enroll_id
        info.backupnum = backupnum
        info.imagepath = imagepath
        info.signatures = signatures
        db.session.commit()

def update_enroll_info2(enroll_id, imagepath, signatures): #新加 2024年1月25日10:41:03

    info = db.session.query(EnrollInfo).filter_by(enroll_id=enroll_id, backupnum=50)
    if info:
        for info in info:
            info.imagepath = imagepath
            info.signatures = signatures
            db.session.commit()



def delete_enroll_info(id):

    info = db.session.query(EnrollInfo).get(id)
    if info:
        db.session.delete(info)
        db.session.commit()
def selectByBackupnum( enroll_id , backupnum):

    return db.session.query(EnrollInfo).filter_by(enroll_id=enroll_id, backupnum=backupnum).first()

def update_by_primary_key_with_blobs(enroll_info):

    info = db.session.query(EnrollInfo).get(enroll_info.id)
    if info:
        info.enroll_id = enroll_info.enroll_id
        info.backupnum = enroll_info.backupnum
        info.imagepath = enroll_info.imagepath
        info.signatures = enroll_info.signatures
        db.session.commit()