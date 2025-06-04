import threading
import time
from Models.MachineCommand import find_pending_command, update_command_status
from Models.Device import get_device_by_serial_num

class SendOrderJob:
    def __init__(self):
        self.running = False
        self.thread = None

    def run(self):
        while self.running:
            print("Polling for pending commands...")
            # Simulate polling logic
            time.sleep(5)

    def start_thread(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
            print("Background job started.")

    def stop_thread(self):
        if self.running:
            self.running = False
            print("Background job stopped.")

    def is_running(self):
        return self.running