class RecordsLog:
    def __init__(self, cmd=None, serial_num=None, count=None, longdex=None, data=None):
        self.cmd = cmd
        self.serial_num = serial_num if serial_num is not None else None
        self.count = count
        self.longdex = longdex
        self.data = data

    def __str__(self):
        return f"RecordsLog [cmd={self.cmd}, serialNum={self.serial_num}, count={self.count}, longdex={self.longdex}, data={self.data}]"
