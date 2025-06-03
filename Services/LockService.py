import json
from datetime import datetime
from Models.LockGroup import LockGroup
from Models.MachineCommand import MachineCommand
from Models.Device import Device
from database import db
class LockGroupService:
    def __init__(self):
        self.session = db.session

    def set_lock_group(self, lock_group):
        # groups = [
        #     {"group": lock_group.group1},
        #     {"group": lock_group.group2},
        #     {"group": lock_group.group3},
        #     {"group": lock_group.group4},
        #     {"group": lock_group.group5}
        # ]

        groups = [
            {"group": self.retNumber(lock_group['group1'])},
            {"group": self.retNumber(lock_group['group2'])},
            {"group": self.retNumber(lock_group['group3'])},
            {"group": self.retNumber(lock_group['group4'])},
            {"group": self.retNumber(lock_group['group5'])}
        ]
        message = {"cmd": "setdevlock", "lockgroup": groups}
        message_str = json.dumps(message)

        devices = self.session.query(Device).all()
        for device in devices:
            machine_command = MachineCommand(content=message_str, name="setdevlock", status=0, send_status=0,
                                             err_count=0, serial=device.serial_num)
            self.session.add(machine_command)
        self.session.commit()
    def retNumber(self,group):
        try:
            return int(group)
        except:
            return 0

