
class UserTemp:
    def __init__(self, enrollId=None,  backupnum=None, admin=None):
        self.enrollId = enrollId
        self.backupnum = backupnum
        self.admin = admin



    def __str__(self):
        return f"UserInfo [enrollId={self.enrollId}, backupnum={self.backupnum}, admin={self.admin}]"
