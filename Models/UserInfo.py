class UserInfo:
    def __init__(self, enroll_id=None, name=None, backupnum=None, admin=None, imagepath=None, record=None):
        self.enroll_id = enroll_id
        self.name = name
        self.backupnum = backupnum
        self.admin = admin
        self.imagepath = imagepath
        self.record = record

    def __str__(self):
        return f"UserInfo [enrollId={self.enroll_id}, name={self.name}, backupnum={self.backupnum}, admin={self.admin}, imagePath={self.imagepath}, record={self.record}]"
