import asyncio
import websockets
from typing import Dict
from Models.DeviceStatus import DeviceStatus

ws_device: Dict[str, DeviceStatus] = {}

class WebSocketPool:

    @staticmethod
    async def get_device_socket_by_sn(device_sn):
        device_status = ws_device.get(device_sn)
        return device_status.websocket

    @staticmethod
    def add_device_and_status(device_sn, device_status):
        ws_device[device_sn] = device_status
        print( "add_device_and_status:" + str(len(ws_device)))

    @staticmethod
    async def send_message_to_device_status(sn, message):
        device_status = ws_device.get(sn)
        conn = device_status.websocket
        if conn is not None:
            await conn.send(message)

    @staticmethod
    def remove_device_status(sn):
        if sn in ws_device:
            del ws_device[sn]
            return True
        else:
            return False

    @staticmethod
    def remove_device_by_websocket(websocket):
        for sn, device_status in list(ws_device.items()):
            if device_status.websocket == websocket:
                del ws_device[sn]
                return sn
        return None

    @staticmethod
    def get_serial_number(websocket):
        for device_status in ws_device.values():
            if device_status.websocket == websocket:
                sn = device_status.device_sn
                del ws_device[sn]
                return sn
        return None

    @staticmethod
    def get_device_status(sn):
        return ws_device.get(sn)

    @staticmethod
    async def send_message_to_all_device_free(message):
        print("Sending message to all free devices")
        for device_status in ws_device.values():
            if device_status.websocket is not None:
                await device_status.websocket.send(message)
