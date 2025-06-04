import json
import uuid
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import base64

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
from Models.Person import Person, insert_person, select_person_by_id, delete_person_by_id, update_person_by_id, select_all as select_all_persons
from Models.MachineCommand import MachineCommand, insert_machine_command, find_pending_command, update_command_status, update_command_status_http
from Models.EnrollInfo import EnrollInfo, insert_enroll_info, get_all_enroll_info, selectByBackupnum, update_enroll_info2, update_by_primary_key_with_blobs
from Models.Records import Record, insert_record, select_all_records, insert_record2
from Models.Msg import Msg
from Services.PersonService import PersonService, PersonServiceImpl

person_ = Person()
enrollinfo = EnrollInfo()
personService = PersonServiceImpl(person=person_, enroll_info=enrollinfo, machine_command=MachineCommand())

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