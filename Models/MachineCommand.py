from datetime import datetime
from database import db
from sqlalchemy import and_

class MachineCommand(db.Model):
    __tablename__ = 'machine_command'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    send_status = db.Column(db.Integer, nullable=False)
    err_count = db.Column(db.Integer, nullable=False)
    run_time = db.Column(db.DateTime, nullable=False)
    gmt_crate = db.Column(db.DateTime, nullable=False)
    gmt_modified = db.Column(db.DateTime, nullable=False)



    def __init__(self, content=None, name=None, status=None, send_status=None, err_count=None, serial=None, run_time=None, gmt_crate=None, gmt_modified=None):
        self.content = content
        self.name = name
        self.status = status
        self.send_status = send_status
        self.err_count = err_count
        self.serial = serial
        # self.run_time = datetime.now() if run_time is None else datetime.strptime(run_time, "%Y-%m-%d %H:%M:%S")
        if run_time is None:
            self.run_time = datetime.now()
        elif isinstance(run_time, datetime):
            self.run_time = run_time
        else:
            self.run_time = datetime.strptime(run_time, "%Y-%m-%d %H:%M:%S")

        if gmt_crate is None:
            self.gmt_crate = datetime.now()
        elif isinstance(gmt_crate, datetime):
            self.gmt_crate = gmt_crate
        else:
            self.gmt_crate = datetime.strptime(gmt_crate, "%Y-%m-%d %H:%M:%S")

        if gmt_modified is None:
            self.gmt_modified = datetime.now()
        elif isinstance(gmt_modified, datetime):
            self.gmt_modified = gmt_modified
        else:
            self.gmt_modified = datetime.strptime(gmt_modified, "%Y-%m-%d %H:%M:%S")

        # self.gmt_crate = datetime.now() if gmt_crate is None else datetime.strptime(gmt_crate, "%Y-%m-%d %H:%M:%S")
        # self.gmt_modified = datetime.now() if gmt_modified is None else datetime.strptime(gmt_modified, "%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"MachineCommand [id={self.id}, serial={self.serial}, name={self.name}, content={self.content}, " \
               f"status={self.status}, sendStatus={self.send_status}, errCount={self.err_count}, runTime={self.run_time}, " \
               f"gmtCrate={self.gmt_crate}, gmtModified={self.gmt_modified}]"

    def update_machine_command(self, machine_command_id, **kwargs):
        # 检索特定的MachineCommand记录
        machine_command = db.session.query(MachineCommand).filter_by(id=machine_command_id).first()
        if machine_command:
            # 更新记录的属性
            for key, value in kwargs.items():
                setattr(machine_command, key, value)

            # 保存更改
            db.session.commit()
        else:
            print(f"No machine command found with id {machine_command_id}")

    def update_machine_command2(self,  **kwargs):
        # 检索特定的MachineCommand记录
        machine_command = db.session.query(MachineCommand).filter_by(id=self.id).first()
        if machine_command:
            # 更新记录的属性
            for key, value in kwargs.items():
                setattr(machine_command, key, value)

            # 保存更改
            db.session.commit()
        else:
            print(f"No machine command found with id {self.id}")
    # 插入数据

    def insert_machine_command(self,machine_command):
        db.session.add(machine_command)
        db.session.commit()
    def insert(self,machine_command):
        db.session.add(machine_command)
        db.session.commit()

    # 查询数据
    def select_machine_command_by_id(self,id):
        return db.session.query(MachineCommand).get(id)

    # 删除数据
    def delete_machine_command_by_id(self,id):
        machine_command = select_machine_command_by_id(id)
        db.session.delete(machine_command)
        db.session.commit()

    # 更新数据
    def update_machine_command_by_id(self,id, **kwargs):
        machine_command = select_machine_command_by_id(id)
        for key, value in kwargs.items():
            setattr(machine_command, key, value)
        db.session.commit()

    # 查找待处理的命令
    def find_pending_command(self,send_status, serial):
        return db.session.query(MachineCommand).filter(
            MachineCommand.status == 0,
            MachineCommand.send_status == send_status,
            MachineCommand.serial == serial,
            MachineCommand.err_count != 3
        ).all()

    @staticmethod
    def add_get_one_user_command(enroll_id, backup_num, serial_num):
        message = f'{{"cmd":"getuserinfo","enrollid":{enroll_id},"backupnum":{backup_num}}}'
        machine_command = MachineCommand(message, "getuserinfo", 0, 0, 0, serial_num)
        db.session.add(machine_command)
        db.session.commit()


def insert_machine_command(machine_command):
    db.session.add(machine_command)
    db.session.commit()


# 查询数据
def select_machine_command_by_id(id):
    print("select_machine_command_by_id")
    print(id)
    return db.session.query(MachineCommand).filter_by(id=id).first()


# 删除数据
def delete_machine_command_by_id(id):
    machine_command = select_machine_command_by_id(id)
    db.session.delete(machine_command)
    db.session.commit()


# 更新数据
def update_machine_command_by_id(id, **kwargs):
    machine_command = select_machine_command_by_id(id)
    for key, value in kwargs.items():
        setattr(machine_command, key, value)
    db.session.commit()


# 查找待处理的命令
def find_pending_command(send_status, serial):
    try:
        # print("find_pending_command")
        ret=db.session.query(MachineCommand).filter(
            MachineCommand.status == 0,
            MachineCommand.send_status == send_status,
            MachineCommand.serial == serial,
            MachineCommand.err_count != 3
        ).all()

        # print(ret)
        return ret
    except Exception as ex:
        print(ex)
        import traceback
        traceback.print_exc()
        return None

def update_command_status(status,send_status,time,machine_command_id):
    machine_command = select_machine_command_by_id(machine_command_id)
    machine_command.status = status
    machine_command.send_status = send_status
    machine_command.run_time = time
    db.session.commit()

def update_machine_command( **kwargs):
    id = kwargs.pop('id', None)
    if id is None:
        print("No id provided")
        return
    # 检索特定的MachineCommand记录
    machine_command = db.session.query(MachineCommand).filter_by(id=id).first()
    if machine_command:
        # 更新记录的属性
        for key, value in kwargs.items():
            setattr(machine_command, key, value)

    # 保存更改
        db.session.commit()
    else:
        print(f"No machine command found with id {id}")

def update_machine_command_o(machine_command):
    id =machine_command.id
    if id is None:
        print("No id provided")
        return
    # 检索特定的MachineCommand记录
    machine_command_ = db.session.query(MachineCommand).filter_by(id=id).first()
    if machine_command_:
        machine_command_.serial = machine_command.serial
        machine_command_.name = machine_command.name
        machine_command_.content =  machine_command.content
        machine_command_.status =  machine_command.status
        machine_command_.send_status = machine_command.send_status
        machine_command_.err_count =  machine_command.err_count
        machine_command_.run_time =  machine_command.run_time
        machine_command_.gmt_crate =  machine_command.gmt_crate
        machine_command_.gmt_modified =  machine_command.gmt_modified
        db.session.commit()
    else:
        print(f"No machine command found with id {id}")

def update_command_status_http(serial, command_type):
    try:
        command = MachineCommand.query.filter(
            and_(
                MachineCommand.serial == serial,
                MachineCommand.name == command_type,
                MachineCommand.status == 1
            )
        ).first()

        if command:
            command.status = 0
            command.gmt_modified = datetime.now()
            db.session.commit()
            return True
        else:
            print(f"No matching command found for SN={serial}, CMD={command_type}")
            return False
    except Exception as e:
        db.session.rollback()
        print("Error updating command:", str(e))
        return False