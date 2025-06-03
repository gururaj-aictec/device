from datetime import datetime
from abc import ABC, abstractmethod

from Models.MachineCommand import MachineCommand
from web_socket.WebSocketPool import WebSocketPool
from Models.EnrollInfo import EnrollInfo
import asyncio
class PersonService(ABC):
    @abstractmethod
    def updateByPrimaryKeySelective(self, record):
        pass

    @abstractmethod
    def updateByPrimaryKey(self, record):
        pass

    @abstractmethod
    def insertSelective(self, person):
        pass

    @abstractmethod
    def insert(self, person):
        pass

    @abstractmethod
    def deleteByPrimaryKey(self, id):
        pass

    @abstractmethod
    def selectByPrimaryKey(self, id):
        pass

    @abstractmethod
    def selectAll(self):
        pass


class PersonServiceImpl():
    def __init__(self, person, enroll_info, machine_command):
        self.person = person
        self.enroll_info = enroll_info
        self.machine_command = machine_command

    def updateByPrimaryKeySelective(self, record):
        return self.person.updateByPrimaryKeySelective(record)

    # Similar methods for other abstract methods...


    # class PersonService:
    #     def __init__(self, machine_command):
    #         self.machine_command = machine_command

    def set_user_to_device(self, enroll_id, name, backupnum, admin, records, device_sn):
            if backupnum != -1:
                machine_command = MachineCommand(name="setuserinfo", status=0, send_status=0, err_count=0,serial=device_sn)
                # machine_command.name = "setuserinfo"
                # machine_command.status = 0
                # machine_command.send_status = 0
                # machine_command.err_count = 0
                # machine_command.serial = device_sn
                # machine_command.gmt_create = datetime.now()
                # machine_command.gmt_modified = datetime.now()

                if self.is_number(records):
                    machine_command.content = f'{{"cmd":"setuserinfo","enrollid":{enroll_id},"name":"{name}","backupnum":{backupnum},"admin":{admin},"record":{records}}}'
                else:
                    machine_command.content = f'{{"cmd":"setuserinfo","enrollid":{enroll_id},"name":"{name}","backupnum":{backupnum},"admin":{admin},"record":"{records}"}}'

                if backupnum == 11 or backupnum == 10:
                    if self.is_number(records):
                        machine_command.content = f'{{"cmd":"setuserinfo","enrollid":{enroll_id},"name":"{name}","backupnum":{backupnum},"admin":{admin},"record":{records}}}'
                    else:
                        machine_command.content = f'{{"cmd":"setuserinfo","enrollid":{enroll_id},"name":"{name}","backupnum":{backupnum},"admin":{admin},"record":“{records}"}}'


                self.machine_command.insert(machine_command)
            else:
                sb = f'{{"cmd":"setusername","count":1,"record":[{{"enrollid":{enroll_id},"name":"{name}"}}]}}'
                print(f'下发用户姓名{sb}')

                machine_command = MachineCommand()
                machine_command.name = "setusername"
                machine_command.status = 0
                machine_command.send_status = 0
                machine_command.err_count = 0
                machine_command.serial = device_sn
                machine_command.gmt_create = datetime.now()
                machine_command.gmt_modified = datetime.now()
                machine_command.content = sb

                self.machine_command.insert(machine_command)

    def set_username_to_device(self, device_sn):
        persons = self.person.select_all()

        print(len(persons))

        sb = []
        for j in range(len(persons)):
            if j == len(persons) - 1 or len(persons) == 1:
                sb.append(f'{{"enrollid":{persons[j].id},"name":"{persons[j].name}"}}')
            else:
                sb.append(f'{{"enrollid":{persons[j].id},"name":"{persons[j].name}"}},')

        sb_str = f'{{"cmd":"setusername","count":{len(persons)},"record":[{"".join(sb)}]}}'
        print(f'下发用户姓名{sb_str}')

        machine_command = MachineCommand()
        machine_command.name = "setusername"
        machine_command.status = 0
        machine_command.send_status = 0
        machine_command.err_count = 0
        machine_command.serial = device_sn
        machine_command.gmt_create = datetime.now()
        machine_command.gmt_modified = datetime.now()
        machine_command.content = sb_str

        self.machine_command.insert(machine_command)
    def setUserToDevice2(self, device_sn):
        user_infos = self.enroll_info.users_to_send_device()

        print(len(user_infos))
        for user_info in user_infos:
            enroll_id = user_info.enroll_id
            name = user_info.name
            backupnum = user_info.backupnum
            admin = user_info.admin
            record = user_info.record

            machine_command = MachineCommand()
            machine_command.name = "setuserinfo"
            machine_command.status = 0
            machine_command.send_status = 0
            machine_command.err_count = 0
            machine_command.serial = device_sn
            machine_command.gmt_create = datetime.now()
            machine_command.gmt_modified = datetime.now()
            if self.is_number(record):
                machine_command.content = f'{{"cmd":"setuserinfo","enrollid":{enroll_id},"name":"{name}","backupnum":{backupnum},"admin":{admin},"record":{record}}}'
            else:
                machine_command.content = f'{{"cmd":"setuserinfo","enrollid":{enroll_id},"name":"{name}","backupnum":{backupnum},"admin":{admin},"record":"{record}"}}'

            if backupnum == 11 or backupnum == 10:

                if self.is_number(record):
                    machine_command.content = f'{{"cmd":"setuserinfo","enrollid":{enroll_id},"name":"{name}","backupnum":{backupnum},"admin":{admin},"record":{record}}}'
                else:
                    machine_command.content = f'{{"cmd":"setuserinfo","enrollid":{enroll_id},"name":"{name}","backupnum":{backupnum},"admin":{admin},"record":“{record}”}}'


            self.machine_command.insert(machine_command)

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    def get_signature(self, enroll_id, device_sn, backupnum):
        asyncio.sleep(0.4)
        message = f'{{"cmd":"getuserinfo","enrollid":{enroll_id},"backupnum":0}}'
        message1 = f'{{"cmd":"getuserinfo","enrollid":{enroll_id},"backupnum":{backupnum}}}'
        device_status = WebSocketPool.get_device_status(device_sn)
        print(f'socket connection {WebSocketPool.get_device_socket_by_sn(device_sn)}')
        if device_status.status == 1:
            device_status.status = 0
            self.update_device(device_sn, device_status)
            if device_status.websocket is not None:
                device_status.websocket.send(message1)
        else:
            asyncio.sleep(0.4)
            device_status.status = 0
            self.update_device(device_sn, device_status)
            if device_status.websocket is not None:
                asyncio.run(WebSocketPool.send_message_to_device_status(device_sn, message))

    @staticmethod
    def get_signature2(enrolls, device_sn):
        for enroll in enrolls:
            message1 = f'{{"cmd":"getuserinfo","enrollid":{enroll.enroll_id},"backupnum":{enroll.backupnum}}}'
            machine_command = MachineCommand(content=message1, name='getuserinfo', status=0, send_status=0, err_count=0, serial=device_sn)
            machine_command.insert(machine_command)  # Insert machine_command to the database


    def delete_user_info_from_device(self, enroll_id, device_sn):
        backupnum = 13
        message = f'{{"cmd":"deleteuser","enrollid":{enroll_id},"backupnum":{backupnum}}}'

        machine_command = MachineCommand()
        machine_command.content = message
        machine_command.name = "deleteuser"
        machine_command.status = 0
        machine_command.send_status = 0
        machine_command.err_count = 0
        machine_command.serial = device_sn
        machine_command.gmt_create = datetime.now()
        machine_command.gmt_modified = datetime.now()

        self.machine_command.insert(machine_command)
        self.person.delete_by_primary_key(enroll_id)
        self.enroll_info.delete_by_enroll_id(enroll_id)

    def update_device(self, sn, device_status):
        if WebSocketPool.get_device_status(sn) is not None:
            WebSocketPool.remove_device_status(sn)
            WebSocketPool.add_device_and_status(sn, device_status)
        else:
            WebSocketPool.add_device_and_status(sn, device_status)