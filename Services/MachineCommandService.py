# from datetime import datetime
# from Models.MachineCommand import MachineCommand
# class MachineCommandService:
#     def __init__(self, machine_command):
#         self.machine_command = machine_command
#
#     def add_machine_command(self, machine_command):
#         self.machine_command.insert(machine_command)
#
#     def add_get_one_user_command(self, enroll_id, backup_num, serial_num):
#         message = f'{{"cmd":"getuserinfo","enrollid":{enroll_id},"backupnum":{backup_num}}}'
#         machine_command = MachineCommand(message, "getuserinfo", 0, 0, 0, serial_num, datetime.now(), datetime.now())
#
#         self.machine_command.insert(machine_command)
