from flask import Flask, jsonify
from Models.Device import Device, insert_device, get_all_devices, get_device_by_id, get_device_by_serial_num, update_device
from app_old import app

@app.route('/device', methods=['POST'])
def create_device(serial_num, status):
    # 这里假设您已经从请求中获取了 serial_num 和 status
    insert_device(serial_num, status)
    return jsonify({"message": "Device created successfully."}), 201

@app.route('/devices', methods=['GET'])
def fetch_devices():
    devices = get_all_devices()
    return jsonify([str(device) for device in devices]), 200

@app.route('/device/<int:id>', methods=['GET'])
def fetch_device(id):
    device = get_device_by_id(id)
    if device:
        return jsonify(str(device)), 200
    else:
        return jsonify({"message": "Device not found."}), 404

@app.route('/device/<string:serial_num>', methods=['GET'])
def fetch_device_by_serial_num(serial_num):
    device = get_device_by_serial_num(serial_num)
    if device:
        return jsonify(str(device)), 200
    else:
        return jsonify({"message": "Device not found."}), 404

@app.route('/device/<int:id>', methods=['PUT'])
def update_existing_device(id,serial_num, status):
    # 这里假设您已经从请求中获取了新的 serial_num 和 status
    update_device(id, serial_num, status)
    return jsonify({"message": "Device updated successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
