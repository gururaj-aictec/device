import json
import uuid

import jsons
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import base64

from Models.AccessDay import get_access_day_by_id, AccessDay, get_all_access_days
from Models.AccessWeek import get_access_week_by_id, AccessWeek
from Services.AccessWeekService import AccessWeekService
from Services.EnrollInfoService import EnrollInfoService
from Services.LockService import LockGroupService
from Services.UserLockService import UserLockService
# from app_old import readConf_
from config.readConf import readConf
from Helpers.log_conf import Logger
from database import db, app
from job.SendOrderJob import SendOrderJob
from flask_sqlalchemy import SQLAlchemy
# Initialize Config
readConf_=readConf()
url=readConf_.GetDBParam()

# Background Job
send_order_job = SendOrderJob()

@app.before_request
def start_thread_once():
    if not send_order_job.is_running():
        print("Starting background job...")
        send_order_job.start_thread()

import atexit
atexit.register(send_order_job.stop_thread)

# Routes
from Models.Device import Device, insert_device, get_all_devices, get_device_by_id, get_device_by_serial_num, update_status_by_primary_key
from Models.Person import Person, insert_person, select_person_by_id, delete_person_by_id, update_person_by_id, \
    select_all as select_all_persons, select_all
from Models.MachineCommand import MachineCommand, insert_machine_command, find_pending_command, update_command_status, update_command_status_http
from Models.EnrollInfo import EnrollInfo, insert_enroll_info, get_all_enroll_info, selectByBackupnum, update_enroll_info2, update_by_primary_key_with_blobs
from Models.Records import Record, insert_record, select_all_records, insert_record2
from Models.Msg import Msg
from Services.PersonService import PersonService, PersonServiceImpl

person_=Person()
enrollinfo=EnrollInfo()
enrollinfoserive=EnrollInfoService( enroll_info=enrollinfo,person=person_)
# machine_command_=MachineCommand()
# machinecommandservice=MachineCommandService(machine_command=MachineCommand)
personService = PersonServiceImpl(person=person_, enroll_info=enrollinfoserive, machine_command=MachineCommand())



@app.route('/device', methods=['POST'])
def create_device():

    data = request.get_json()  # Get data from JSON body
    serial_num = data.get('serial_num')
    status = data.get('status')
    insert_device(serial_num, status)
    return jsonify({"message": "Device created successfully."}), 201
@app.route('/device', methods=['GET'])
def get_all_device():
    print("get all device")
    update_status_by_primary_key(62, 1)
    device_list = get_all_devices()
    device_list = [device.to_dict() for device in device_list]  # Convert each Device to a dictionary
    return jsons.dump(Msg.success().add("device", device_list))



@app.route('/enrollInfo', methods=['GET'])
def get_all_enrollinfo():
    enroll_infoes = get_all_enroll_info() # Person.query.all()
    enroll_infoes = [enroll_info.to_dict() for enroll_info in enroll_infoes]
    return jsons.dump(Msg.success().add("enrollInfo", enroll_infoes))



@app.route('/sendWs', methods=['GET'])
def send_ws():
    device_sn = request.args.get('deviceSn')
    print(("device_sn:"+device_sn))
    message = "{\"cmd\":\"getuserlist\",\"stn\":true}"

    device_list = Device.query.all()
    for device in device_list:
        machine_command = MachineCommand(
            name="getuserlist",
            status=0,
            send_status=0,
            err_count=0,
            serial=device.serial_num,
            gmt_crate=datetime.now(),
            gmt_modified=datetime.now(),
            content=message
        )
        print(machine_command)
        db.session.add(machine_command)
    db.session.commit()

    return jsons.dump(Msg.success())





@app.route('/addPerson', methods=['POST'])
def add_person():
    person_temp = request.form
    pic = request.files['pic']
    # path = "C:/dynamicface/picture/"
    path=readConf().GetUploadParam()
    photo_name = ""
    new_name = ""
    if pic:
        if pic.filename:
            photo_name = secure_filename(pic.filename)
            new_name = str(uuid.uuid4()) + photo_name[photo_name.rfind('.'):]
            photo_file = os.path.join(path, new_name)
            pic.save(photo_file)

    person = {
        'id': person_temp.get('userId'),
        'name': person_temp.get('name'),
        'roll_id': person_temp.get('privilege')
    }
    existing_person = select_person_by_id(person_temp.get('userId'))

    if not existing_person:
        insert_person(**person)

    if person_temp.get('password'):
        enroll_info_temp2 = {
            'backupnum': 10,
            'enroll_id': person_temp.get('userId'),
            'signatures': person_temp.get('password')
        }
        insert_enroll_info(**enroll_info_temp2)

    if person_temp.get('cardNum'):
        enroll_info_temp3 = {
            'backupnum': 11,
            'enroll_id': person_temp.get('userId'),
            'signatures': person_temp.get('cardNum')
        }
        insert_enroll_info(**enroll_info_temp3)

    if new_name:
        with open(os.path.join(path, new_name), "rb") as image_file:
            base64_str = base64.b64encode(image_file.read()).decode()

        enroll_info_temp = {
            'backupnum': 50,
            'enroll_id': person_temp.get('userId'),
            'imagepath': new_name,
            'signatures': base64_str
        }
        insert_enroll_info(**enroll_info_temp)
    else:
        enroll_info_temp = {
            'backupnum': 50,
            'enroll_id': person_temp.get('userId'),
            'imagepath': "",
            'signatures': ""
        }
        insert_enroll_info(**enroll_info_temp)
    return jsons.dump(Msg.success())


@app.route('/getUserInfo', methods=['GET'])
def get_user_info():
    print("Get user info")
    device_sn = request.args.get('deviceSn')
    persons = Person.query.all()
    enrolls_prepared = []
    for person in persons:
        enroll_infos = EnrollInfo.query.filter_by(enroll_id=person.id).all()
        for enroll_info in enroll_infos:
            if enroll_info.enroll_id and enroll_info.backupnum:
                enrolls_prepared.append(enroll_info)
    print("Collecting user data: ", enrolls_prepared)
    PersonServiceImpl.get_signature2(enrolls_prepared, device_sn)

    return jsons.dump(Msg.success())


@app.route('/sendGetUserInfo', methods=['GET'])
def send_get_user_info():
    enroll_id = request.args.get('enrollId', type=int)
    backupnum = request.args.get('backupNum', type=int)
    device_sn = request.args.get('deviceSn')

    device_list = Device.query.all()
    print("Device info: ", device_list)

    message = {"cmd": "getuserinfo", "enrollid": enroll_id, "backupnum": backupnum}

    MachineCommand.add_get_one_user_command(enroll_id, backupnum, device_sn)

    return jsons.dump(Msg.success())


@app.route('/setPersonToDevice', methods=['GET']) #2024年1月8日16:53:53
def send_set_user_info():
    device_sn = request.args.get('deviceSn')

    personService.setUserToDevice2(device_sn)

    return jsons.dump(Msg.success())


@app.route('/setUsernameToDevice', methods=['GET']) #2024年1月8日18:06:22
def set_username_to_device():
    device_sn = request.args.get('deviceSn')

    personService.set_username_to_device(device_sn)

    return jsons.dump(Msg.success())


@app.route('/getDeviceInfo', methods=['GET']) #2024年1月8日18:06:22
def get_device_info():
    device_sn = request.args.get('deviceSn')

    message ='{"cmd":"getdevinfo"}'
    machine_command = MachineCommand(content=message, name="getdevinfo", status=0, send_status=0, err_count=0, serial = device_sn)
    machine_command.insert_machine_command(machine_command)
    return jsons.dump(Msg.success())


@app.route('/setOneUser', methods=['GET']) #2024年1月8日18:06:22
def set_one_user_to():
    enroll_id = request.args.get('enrollId', type=int)
    backupnum = request.args.get('backupNum', type=int)
    device_sn = request.args.get('deviceSn')

    # print("Set one user to device: ", enroll_id, backupnum, device_sn)
    person = select_person_by_id(enroll_id)
    enroll_info = selectByBackupnum(enroll_id, backupnum)
    # print("Enroll info: ", enroll_info)
    # print("Enroll info: ", enroll_info.signatures)
    if enroll_info is not None:
        personService.set_user_to_device(enroll_id, person.name, backupnum, person.roll_id, enroll_info.signatures,device_sn)
        return jsons.dump(Msg.success())
    elif backupnum == -1:
        personService.set_user_to_device(enroll_id, person.name, backupnum, 0, "", device_sn)
        return jsons.dump(Msg.success())
    else:
        return jsons.dump(Msg.fail())


@app.route('/deletePersonFromDevice', methods=['GET'])
def delete_device_user_info():
    enroll_id = request.args.get('enrollId', type=int)
    device_sn = request.args.get('deviceSn')

    print("Deleting user devicesn: ", device_sn)
    personService.delete_user_info_from_device(enroll_id, device_sn)

    return jsons.dump(Msg.success())


@app.route('/initSystem', methods=['GET']) #todo 2024年1月8日18:06:22 没有测试
def init_system():
    device_sn = request.args.get('deviceSn')

    print("Initialization request")
    # 创建消息
    message = '{"cmd": "enabledevice"}'
    message2 = '{"cmd": "settime", "cloudtime": "2020-12-23 13:49:30"}'
    s4 = '{"cmd": "settime", "cloudtime": "2016-03-25 13:49:30"}'
    s2 = '{"cmd": "setdevinfo", "deviceid": 1, "language": 0, "volume": 0, "screensaver": 0, "verifymode": 0, "sleep": 0,"userfpnum": 3, "loghint": 1000, "reverifytime": 0}'
    s5 = '{"cmd": "enableuser", "enrollid": 1, "enflag": 0}'
    s6 = '{"cmd": "getusername", "enrollid": 1}'
    message = '{"cmd": "initsys"}'

    machine_command = MachineCommand(content=message, name="initsys", status=0, send_status=0, err_count=0, serial=device_sn)

    machine_command.insert_machine_command(machine_command)

    return jsons.dump(Msg.success())


@app.route('/getAllLog', methods=['GET'])
def getAllLog():
    device_sn = request.args.get('deviceSn')

    message = '{"cmd":"getalllog","stn":true}'
    # messageTemp = '{"cmd":"getalllog","stn":true,"from":"2020-12-03","to":"2020-12-30"}'

    machine_command = MachineCommand()
    machine_command.content = message
    machine_command.name = "getalllog"
    machine_command.status = 0
    machine_command.send_status = 0
    machine_command.err_count = 0
    machine_command.serial = device_sn
    machine_command.gmt_crate = datetime.now()
    machine_command.gmt_modified = datetime.now()

    machine_command.insert_machine_command(machine_command)
    return jsons.dump(Msg.success())

@app.route('/getNewLog', methods=['GET'])
def get_new_log():
    device_sn = request.args.get('deviceSn')
    message = '{"cmd": "getnewlog", "stn": true}'
    machine_command = MachineCommand(content=message, name="getnewlog", status=0, send_status=0, err_count=0,serial=device_sn)
    machine_command.insert_machine_command(machine_command)
    return jsons.dump(Msg.success())

from  Services.AccessDayService import  AccessDayService
@app.route('/setAccessDay', methods=['POST'])
def set_access_day():
    access_day = request.form.to_dict()
    print(access_day)
    if get_access_day_by_id(access_day['id']) is not None:
        return jsons.dump(Msg.fail())
    access_day_instance = AccessDay(**access_day)
    db.session.add(access_day_instance)
    # insert_access_day(access_day)
    accessDayService=AccessDayService()
    accessDayService.set_access_day()
    return jsons.dump(Msg.success())


@app.route('/setAccessWeek', methods=['POST'])
def set_access_week():
    access_week = request.form.to_dict()  # assumes you're receiving JSON data in the request body
    if get_access_week_by_id(access_week['id']) is not None:
        return jsons.dump(Msg.fail())
    access_week_instance = AccessWeek(**access_week)
    db.session.add(access_week_instance)
    accessWeekService = AccessWeekService()
    accessWeekService.set_access_week()
    return jsons.dump(Msg.success())

from flask import send_from_directory  #2024年1月10日23:37:16
@app.route('/img/<filename>', methods=['GET'])
def upload_file(filename):
    path = readConf().GetUploadParam()
    return send_from_directory(path, filename)

@app.route('/setLocckGroup', methods=['POST'])
def set_lock_group():
    lock_group =  request.form.to_dict()
    lockGroupService = LockGroupService()
    lockGroupService.set_lock_group(lock_group)
    return jsons.dump(Msg.success())




@app.route('/setUserLock', methods=['POST'])  #2024年1月10日23:37:16
def set_user_lock():
    user_lock =  request.form.to_dict()
    userLockService = UserLockService()
    userLockService.set_user_lock(user_lock, user_lock['starttime'], user_lock['endtime'])
    return jsons.dump(Msg.success())

from Models.Page import PageInfo
@app.route('/emps', methods=['GET'])
def get_all_person_from_db():
    pn = request.args.get('pn', default=1, type=int)
    person_list = select_all()
    enroll_list = get_all_enroll_info()  #EnrollInfo.select_all()
    emps = []
    for person in person_list:
        for enroll_info in enroll_list:
            if person.id == enroll_info.enroll_id and enroll_info.backupnum == 50:
                emps.append({
                    'enrollId': person.id,
                    'admin': person.roll_id,
                    'name': person.name,
                    'imagePath': enroll_info.imagepath
                })
    page=PageInfo(emps,5)
    # return jsons.dump(success=True, pageInfo={'emps': emps, 'pn': pn})  # you'll need to implement your own paging
    return jsons.dump(Msg.success().add("pageInfo", page))
#Msg.success().add("device", device_list)

@app.route('/records', methods=['GET'])
def get_all_log_from_db():
    pn = request.args.get('pn', default=1, type=int)
    records = select_all_records()

    records = [record.to_dict() for record in records]
    print(records)
    pageInfo=PageInfo(records,5)
    # print(pageInfo)
    return jsons.dump(Msg.success().add("pageInfo", pageInfo))

@app.route('/accessDays', methods=['GET'])
def get_access_day_from_db():
    access_days = get_all_access_days()
    access_days = [access_day.to_dict() for access_day in access_days]  # Convert each Device to a dictionary
    # print(access_days)
    return jsons.dump(Msg.success().add("accessdays", access_days))



@app.route('/uploadUserToDevice', methods=['POST']) #todo:这个可能没有用 2024年1月11日09:57:54
def upload_user_to_device():
    enroll_id = request.args.get('enrollId', type=int)
    person = Person.selectByPrimaryKey(enroll_id)
    # you'll need to implement the actual upload function
    return jsons.dump(Msg.success())




@app.route('/openDoor', methods=['GET'])
def open_door():
    door_num = request.args.get('doorNum', type=int)
    device_sn = request.args.get('deviceSn')
    message = json.dumps({'cmd': 'opendoor', 'doornum': door_num})
    machine_command = MachineCommand(content=message, name="opendoor", status=0, send_status=0, err_count=0,serial=device_sn)
    machine_command.insert_machine_command(machine_command)
    return jsons.dump(Msg.success())


@app.route('/getDevLock', methods=['GET'])
def get_dev_lock():
    device_sn = request.args.get('deviceSn')
    message =json.dumps({"cmd": "getdevlock"})
    machine_command = MachineCommand(content=message, name="getdevlock", status=0, send_status=0, err_count=0,serial=device_sn)
    machine_command.insert_machine_command(machine_command)
    return jsons.dump(Msg.success())


@app.route('/getUserLock', methods=['GET'])
def get_user_lock():
    enroll_id = request.args.get('enrollId', type=int)
    device_sn = request.args.get('deviceSn')
    message = json.dumps({"cmd": "getuserlock", "enrollid": enroll_id})
    machine_command = MachineCommand(content=message, name="getuserlock", status=0, send_status=0, err_count=0, serial=device_sn)
    machine_command.insert_machine_command(machine_command)
    return jsons.dump(Msg.success())


@app.route('/cleanAdmin', methods=['GET'])
def clean_admin():
    device_sn = request.args.get('deviceSn')
    message =json.dumps({"cmd": "cleanadmin"})
    machine_command = MachineCommand(content=message, name="cleanadmin", status=0, send_status=0, err_count=0, serial=device_sn)
    machine_command.insert_machine_command(machine_command)
    return jsons.dump(Msg.success())

@app.route('/')
def index():
    APP_PATH = request.base_url[:-1]
    return render_template("index.html", APP_PATH=APP_PATH)

@app.route('/logRecords')
def logRecords():
    device_sn = request.args.get('deviceSn')
    APP_PATH = request.base_url[:-10]
    return render_template("logRecords.html", APP_PATH=APP_PATH, deviceSn=device_sn)

@app.route('/device/register', methods=['POST'])
def register_device():
    data = request.get_json()
    sn = data.get('sn')

    if not sn:
        return jsonify({"success": False, "reason": "Missing SN"}), 400

    d1 = get_device_by_serial_num(sn)
    if d1 is None:
        insert_device(sn, status=1)
    else:
        update_status_by_primary_key(d1.id, 1)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'result': True, 'cloudtime': current_time})

@app.route('/log/upload', methods=['POST'])
def upload_log():
    json_node = request.get_json()
    sn = json_node["sn"]
    count = json_node["count"]
    record_all = []

    if count > 0:
        for record in json_node["record"]:
            enroll_id = record["enrollid"]
            time_str = record["time"]
            mode = record["mode"]
            in_out = record["inout"]
            event = record["event"]
            temperature = round(record.get("temp", 0) / 10, 1) if "temp" in record else 0

            rec = Record(
                device_serial_num=sn,
                enroll_id=enroll_id,
                event=event,
                intOut=in_out,
                mode=mode,
                records_time=time_str,
                temperature=temperature
            )
            record_all.append(rec)

        for r in record_all:
            insert_record(r)

    return jsonify({
        'ret': 'sendlog',
        'result': True,
        'cloudtime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/user/upload', methods=['POST'])
def upload_user_info():
    json_node = request.get_json()
    sn = json_node["sn"]
    backupnum = json_node["backupnum"]
    signatures = json_node["record"]

    enroll_id = json_node["enrollid"]
    name = json_node["name"]
    roll_id = json_node["admin"]

    person = {'id': enroll_id, 'name': name, 'roll_id': roll_id}
    if select_person_by_id(enroll_id) is None:
        insert_person(**person)
    else:
        from Models.Person import update_by_primary_key
        update_by_primary_key(person)

    enroll_info = {
        'enroll_id': enroll_id,
        'backupnum': backupnum,
        'signatures': signatures
    }

    if backupnum == 50:
        pic_name = str(uuid.uuid4())
        flag = base64_to_image(json_node["record"], pic_name)
        enroll_info["imagepath"] = pic_name + ".jpg"

    if selectByBackupnum(enroll_id, backupnum) is None:
        insert_enroll_info(**enroll_info)
    else:
        from Models.EnrollInfo import update_by_primary_key_with_blobs
        update_by_primary_key_with_blobs(enroll_info)

    return jsonify({
        'ret': 'senduser',
        'result': True,
        'cloudtime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/command/pending', methods=['GET'])
def get_pending_command():
    device_sn = request.args.get('deviceSn')
    command = find_pending_command(0, device_sn)

    if command:
        update_command_status(0, 1, datetime.now(), command[0].id)
        return jsonify({'command': command[0].content})
    else:
        return jsonify({'command': None})

@app.route('/command/ack', methods=['POST'])
def ack_command():
    data = request.get_json()
    ret = data.get('ret')
    sn = data.get('sn')

    if ret and sn:
        success = update_command_status_http(sn, ret)
        return jsonify({'success': success})
    else:
        return jsonify({'success': False}), 400

def base64_to_image(base64_string, pic_name):
    try:
        image_data = base64.b64decode(base64_string)
        path = readConf_.GetUploadParam()
        with open(os.path.join(path, pic_name + '.jpg'), 'wb') as f:
            f.write(image_data)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("Starting Flask app without WebSocket support...")
    app.run(debug=True, host='0.0.0.0', port=7788)