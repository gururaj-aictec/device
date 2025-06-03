import threading
import time
from datetime import datetime

from Models.MachineCommand import MachineCommand,find_pending_command,update_command_status,update_machine_command,update_machine_command_o
from Models.Device import Device,get_device_by_serial_num
from web_socket.WebSocketPool import WebSocketPool,ws_device
from database import db,app
class SendOrderJob(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        # self.machine_command_mapper = machine_command_mapper
        # self.device_mapper = device_mapper
        self.wd_list = {}  # WebSocketPool.wsDevice
        self._thread=None

    def run_job(self):
        print("SendOrderJob start running")
        while not self.stop_event.is_set():
            # print("SendOrderJob start running-----"+datetime.now().strftime('%Y-%m-%d %H:%M:%S') +" wd_list len:"+ str(len(self.wd_list)))
            for key, device_status in self.wd_list.items():
                with app.app_context():
                    print(device_status)
                    try:
                        print(key)
                        in_sending = find_pending_command(0, key)
                        # print("in_sending",in_sending)
                        if in_sending:
                            pending_command = find_pending_command(1, key)
                            # print(" pending_command")
                            # print(pending_command)
                            # print(len(pending_command))
                            if not pending_command:
                                print(" not pending_command")
                                if isinstance(device_status, dict):
                                    websock = device_status['websocket']
                                    print(websock)
                                    websock.send(in_sending[0].content)
                                else:
                                    websock = device_status.websocket
                                    print(websock)
                                    websock.send(in_sending[0].content)

                                print(" not pending_command send")
                                now = datetime.fromtimestamp(time.time())
                                update_command_status(0, 1, now,in_sending[0].id)
                            elif len(pending_command) == 1:
                                print(pending_command[0].run_time)
                                # run_time = datetime.strptime(pending_command[0].run_time, '%Y-%m-%d %H:%M:%S')
                                run_time =pending_command[0].run_time
                                now = datetime.fromtimestamp(time.time())
                                print(run_time)
                                print(now)
                                difference = (now - run_time).total_seconds()
                                print(difference)
                                if difference > 20: #20

                                    if pending_command[0].err_count < 3:
                                        machine_command = pending_command[0]
                                        machine_command.err_count += 1
                                        machine_command.run_time = now

                                        update_machine_command_o(machine_command)
                                        device = get_device_by_serial_num(pending_command[0].serial)
                                        print("pending_command[0].err_count < 3")
                                        print(device)
                                        if device.status != 0:
                                            print(" device.status != 0")
                                            print("device_status1")
                                            #print(device_status)
                                            if isinstance(device_status,dict):
                                                websock = device_status['websocket']
                                                print(websock)
                                                websock.send(pending_command[0].content)
                                            else:
                                                websock = device_status.websocket
                                                print(websock)
                                                websock.send(pending_command[0].content)
                                    else:
                                        print("pending_command[0].err_count > 3")
                                        print(device)
                                        machine_command = pending_command[0]
                                        machine_command.err_count += 1
                                        update_machine_command_o(machine_command)
                                else:
                                    print(" difference < 20:" + str(difference))
                        else:
                            print("in_sending", in_sending)
                            pending_command = find_pending_command(1, key)
                            if pending_command:
                                if (datetime.now() - pending_command[0].run_time).total_seconds() > 20:
                                    if pending_command[0].err_count < 3:
                                        now = datetime.fromtimestamp(time.time())
                                        machine_command = pending_command[0]
                                        machine_command.err_count += 1
                                        machine_command.run_time = now
                                        update_machine_command_o(machine_command)
                                        device = get_device_by_serial_num(pending_command[0].serial)
                                        if device.status != 0:
                                            print("device_status2")
                                            if isinstance(device_status, dict):
                                                websock = device_status['websocket']
                                                print(websock)
                                                websock.send(pending_command[0].content)
                                            else:
                                                websock = device_status.websocket
                                                print(websock)
                                                websock.send(pending_command[0].content)

                                    else:
                                        machine_command = pending_command[0]
                                        machine_command.err_count += 1
                                        update_machine_command_o(machine_command)

                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        print(e)

            time.sleep(1)  # Avoid high CPU usage

    def stop(self):
        self.stop_event.set()

    # def start_thread(self):
    #     self.start()

    def start_thread(self):
        if self._thread is None or not self._thread.is_alive():
            print("SendOrderJob start running-start_thread")
            self.wd_list=ws_device
            self._thread = threading.Thread(target=self.run_job)
            self._thread.start()

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()
    def stop_thread(self):
        self.stop()
