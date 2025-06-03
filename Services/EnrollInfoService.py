from Models.UserInfo import UserInfo
class EnrollInfoService:
    def __init__(self, enroll_info, person):
        self.enroll_info_mapper = enroll_info
        self.person_mapper = person

    def delete_primary_key(self, id):
        return self.enroll_info_mapper.delete_primary_key(id)

    def insert_selective(self, record):
        return self.enroll_info_mapper.insert_selective(record)

    def select_primary_key(self, id):
        return self.enroll_info_mapper.select_primary_key(id)

    def update_primary_key_selective(self, record):
        return self.enroll_info_mapper.update_primary_key_selective(record)

    def update_primary_key_with_blobs(self, record):
        return self.enroll_info_mapper.update_primary_key_with_blobs(record)

    def insert(self, enrollid, backupnum, imagepath, signature):
        return self.enroll_info_mapper.insert(enrollid, backupnum, imagepath, signature)

    def select_backupnum(self, enroll_id, backupnum):
        return self.enroll_info_mapper.select_backupnum(enroll_id, backupnum)

    def users_to_send_device(self):
        persons = self.person_mapper.select_all()
        enroll_infos = self.enroll_info_mapper.select_all()
        user_infos = []

        for person in persons:
            for enroll_info in enroll_infos:
                if person.id == enroll_info.enroll_id:
                    user_info = UserInfo()
                    user_info.admin = person.roll_id
                    user_info.backupnum = enroll_info.backupnum
                    user_info.enroll_id = person.id
                    user_info.name = person.name
                    user_info.record = enroll_info.signatures

                    user_infos.append(user_info)

        return user_infos

    def select_all(self):
        return self.enroll_info_mapper.select_all()

    def select_by_enroll_id(self, enroll_id):
        return self.enroll_info_mapper.select_by_enroll_id(enroll_id)

    def update_by_enroll_id_and_backup_num(self, signatures, enroll_id, backupnum):
        return self.enroll_info_mapper.update_by_enroll_id_and_backup_num(signatures, enroll_id, backupnum)

    def delete_by_enroll_id(self, id):
        return self.enroll_info_mapper.delete_by_enroll_id(id)
