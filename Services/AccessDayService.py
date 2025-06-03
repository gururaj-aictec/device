import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from Models.AccessDay import AccessDay
from Models.MachineCommand import MachineCommand
from Models.Device import Device
from database import db
class AccessDayService:
    def __init__(self):

        self.session =db.session

    def delete_primary_key(self, id):
        self.session.query(AccessDay).filter(AccessDay.id == id).delete()
        self.session.commit()

    def insert(self, record: AccessDay):
        self.session.add(record)
        self.session.commit()

    def insert_selective(self, record: AccessDay):
        if record.id:
            self.session.merge(record)
        else:
            self.session.add(record)
        self.session.commit()

    def select_primary_key(self, id):
        return self.session.query(AccessDay).filter(AccessDay.id == id).first()

    def update_primary_key_selective(self, record: AccessDay):
        self.session.merge(record)
        self.session.commit()

    def update_primary_key(self, record: AccessDay):
        self.session.merge(record)
        self.session.commit()

    def select_all(self):
        return self.session.query(AccessDay).all()

    def set_access_day(self):
        access_days = self.select_all()
        access_days_temp = access_days[:]
        if len(access_days) < 8:
            for i in range(len(access_days), 8):
                access_day1 = {
                    "id": i + 1,
                    "start_time1": "00:00",
                    "end_time1": "00:00",
                    "start_time2": "00:00",
                    "end_time2": "00:00",
                    "start_time3": "00:00",
                    "end_time3": "00:00",
                    "start_time4": "00:00",
                    "end_time4": "00:00",
                    "start_time5": "00:00",
                    "end_time5": "00:00",
                }
                access_days_temp.append(access_day1)

        message = {"cmd": "setdevlock", "dayzone": []}
        print("access_days_temp")
        print(access_days_temp)
        for i in range(len(access_days_temp)):
            if isinstance(access_days_temp[i], dict):
                day = {
                    "day": [
                        {"section": access_days_temp[i]['start_time1'] + "~" + access_days_temp[i]['end_time1']},
                        {"section": access_days_temp[i]['start_time2'] + "~" + access_days_temp[i]['end_time2']},
                        {"section": access_days_temp[i]['start_time3'] + "~" + access_days_temp[i]['end_time3']},
                        {"section": access_days_temp[i]['start_time4'] + "~" + access_days_temp[i]['end_time4']},
                        {"section": access_days_temp[i]['start_time5'] + "~" + access_days_temp[i]['end_time5']},
                    ]
                }
            else:
                day = {
                    "day": [
                        {"section": access_days_temp[i].start_time1 + "~" + access_days_temp[i].end_time1},
                        {"section": access_days_temp[i].start_time2 + "~" + access_days_temp[i].end_time2},
                        {"section": access_days_temp[i].start_time3 + "~" + access_days_temp[i].end_time3},
                        {"section": access_days_temp[i].start_time4 + "~" + access_days_temp[i].end_time4},
                        {"section": access_days_temp[i].start_time5 + "~" + access_days_temp[i].end_time5},
                    ]
                }
            message["dayzone"].append(day)

        message_str = json.dumps(message)
        print(message_str)
        # Add MachineCommand records
        devices = self.session.query(Device).all()
        for device in devices:
            machine_command = MachineCommand(content=message_str,
                                             name="setdevlock",
                                             status=0,
                                             send_status=0,
                                             err_count=0,
                                             serial=device.serial_num
                                             )
            self.session.add(machine_command)
        self.session.commit()

