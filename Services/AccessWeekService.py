import json
from Models.AccessWeek import AccessWeek
from Models.MachineCommand import MachineCommand
from Models.Device import Device
from database import db
from datetime import datetime

class AccessWeekService:
    def __init__(self):
        self.session = db.session

    def delete_primary_key(self, id):
        self.session.query(AccessWeek).filter(AccessWeek.id == id).delete()
        self.session.commit()

    def insert(self, record: AccessWeek):
        self.session.add(record)
        self.session.commit()

    def insert_selective(self, record: AccessWeek):
        if record.id:
            self.session.merge(record)
        else:
            self.session.add(record)
        self.session.commit()

    def select_primary_key(self, id):
        return self.session.query(AccessWeek).filter(AccessWeek.id == id).first()

    def update_primary_key_selective(self, record: AccessWeek):
        self.session.merge(record)
        self.session.commit()

    def update_primary_key(self, record: AccessWeek):
        self.session.merge(record)
        self.session.commit()
    def select_all_access_week(self):
        return self.session.query(AccessWeek).all()

    def set_access_week(self):
        weeks = []
        access_weeks = self.select_all_access_week()
        access_weeks_temp = access_weeks[:]

        for i in range(len(access_weeks), 8):
            access_week = AccessWeek(id=i+1, monday=0, tuesday=0, wednesday=0, thursday=0, friday=0, saturday=0, sunday=0)
            access_weeks_temp.append(access_week)

        for i in range(len(access_weeks_temp)):
            week = {
                "week": [
                    {"day": access_weeks_temp[i].sunday},
                    {"day": access_weeks_temp[i].monday},
                    {"day": access_weeks_temp[i].tuesday},
                    {"day": access_weeks_temp[i].wednesday},
                    {"day": access_weeks_temp[i].thursday},
                    {"day": access_weeks_temp[i].friday},
                    {"day": access_weeks_temp[i].saturday},
                ]
            }
            weeks.append(week)

        message = {"cmd": "setdevlock", "weekzone": weeks}
        message_str = json.dumps(message)

        devices = self.session.query(Device).all()
        for device in devices:
            machine_command = MachineCommand(content=message_str, name="setdevlock", status=0, send_status=0, err_count=0, serial=device.serial_num)
            self.session.add(machine_command)
        self.session.commit()
