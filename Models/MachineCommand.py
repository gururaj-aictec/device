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

def insert_machine_command(machine_command):
    db.session.add(machine_command)
    db.session.commit()

def select_machine_command_by_id(id):
    return db.session.query(MachineCommand).filter_by(id=id).first()

def find_pending_command(send_status, serial):
    return db.session.query(MachineCommand).filter(
        MachineCommand.status == 0,
        MachineCommand.send_status == send_status,
        MachineCommand.serial == serial,
        MachineCommand.err_count != 3
    ).all()

def update_command_status(status, send_status, time, machine_command_id):
    mc = select_machine_command_by_id(machine_command_id)
    mc.status = status
    mc.send_status = send_status
    mc.run_time = time
    db.session.commit()

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