import json
from typing import Dict, Any, List
class Msg:
    def __init__(self, code=0, msg='', extend=None):
        self.code = code
        self.msg = msg
        self.extend = extend if extend is not None else {}

    def to_dict(self):
        return {
            'code': self.code,
            'msg': self.msg,
            'extend': self.extend
        }
    @staticmethod
    def success():
        return Msg(100, "Success!")

    @staticmethod
    def fail():
        return Msg(200, "Fail!")

    def add(self, key: str, value: Any):
        self.extend[key] = value
        return self
