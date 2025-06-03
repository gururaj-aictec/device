class SetUserReturnInfo:
    def __init__(self, ret=None, sn=None, result=None):
        self.ret = ret
        self.sn = sn
        self.result = result

    def __str__(self):
        return f"SetUserReturnInfo [ret={self.ret}, sn={self.sn}, result={self.result}]"
