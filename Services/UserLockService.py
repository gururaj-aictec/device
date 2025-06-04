from datetime import datetime
import json
from Models.UserLock import UserLock
from Models.MachineCommand import MachineCommand
from Models.Device import Device
from database import db


# from  app_old import  db
class UserLockService:
    def __init__(self):
        self.session = db.session

    def set_user_lock(self, user_lock, start_time, end_time):
        print(user_lock)
        record = {
            "enrollid": int(user_lock["enrollId"]),  # user_lock["enrollId"],  # enroll_id,
            "weekzone": int(user_lock["weekZone"]),  # user_lock["weekZone"],
            "group": int(user_lock["group"]),
            "starttime": f"{start_time} 00:00:00",
            "endtime": f"{end_time} 00:00:00"
        }

        message = {"cmd": "setuserlock", "count": 1, "record": [record]}
        message_str = json.dumps(message)

        devices = self.session.query(Device).all()
        for device in devices:
            machine_command = MachineCommand(content=message_str, name="setuserlock", status=0, send_status=0, err_count=0, serial=device.serial_num)
            self.session.add(machine_command)
        self.session.commit()
