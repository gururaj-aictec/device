

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database import db
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_num = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return "Device [id={}, serialNum={}, status={}]".format(self.id, self.serial_num, self.status)

    def to_dict(self):
        return {
            'id': self.id,
            'serialNum': self.serial_num,
            'status': self.status
        }

    # def __getitem__(self, index):
    #     print("self.contents[index]")
    #     return self.contents[index]
    def insert_device(serial_num, status):
        device = Device(serial_num=serial_num, status=status)
        db.session.add(device)
        db.session.commit()

    # 查询所有设备
    def get_all_devices(self):
        return db.session.query(Device).all()

    # 根据主键查询设备
    def get_device_by_id(self,id):
        return db.session.query(Device).filter_by(id)

    # 根据序列号查询设备
    def get_device_by_serial_num(self,serial_num):
        return db.session.query(Device).filter_by(serial_num=serial_num).first()

    # 更新设备信息
    def update_device(self,id, serial_num, status):
        device = db.session.query(Device).filter_by(id)
        if device:
            device.serial_num = serial_num
            device.status = status
            db.session.commit()

    # 插入新的设备
def insert_device(serial_num, status):
    device = Device(serial_num=serial_num, status=status)
    db.session.add(device)
    db.session.commit()

# 查询所有设备
def get_all_devices():

    return Device.query.all()

# 根据主键查询设备
def get_device_by_id(id):
    return db.session.query(Device).filter_by(id)

# 根据序列号查询设备
def get_device_by_serial_num(serial_num):
    return db.session.query(Device).filter_by(serial_num=serial_num).first()

# 更新设备信息
def update_device(id, serial_num, status):
    device = db.session.query(Device).filter_by(id)
    if device:
        device.serial_num = serial_num
        device.status = status
        db.session.commit()
def update_status_by_primary_key(id,  status):
    device = db.session.query(Device).filter_by(id=id).first()

    if device:
        device.status = status
        db.session.commit()