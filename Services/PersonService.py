from Models.Person import Person
from Models.EnrollInfo import EnrollInfo
from Models.MachineCommand import MachineCommand

class PersonService:
    def __init__(self, person=None, enroll_info=None, machine_command=None):
        self.person = person
        self.enroll_info = enroll_info
        self.machine_command = machine_command

class PersonServiceImpl(PersonService):
    def setUserToDevice2(self, device_sn):
        # Replace with real logic
        pass

    def set_username_to_device(self, device_sn):
        # Replace with real logic
        pass

    def delete_user_info_from_device(self, enroll_id, device_sn):
        # Replace with real logic
        pass