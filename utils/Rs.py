# -*- coding = utf-8 -*-
# @time: 2024/6/28 下午7:49
# @author: Ma Huibo
# @email mhb0409@qq.com
# @file: Rs.py
class Rs:
    def __init__(self):
        self.data = None
        self.message = None
        self.code = None

    def ok(self, message="请求成功", data=None):
        self.code = 200
        self.message = message
        self.data = data
        return self.__call__()

    def fail(self, message="请求失败", data=None):
        self.code = 500
        self.message = message
        self.data = data
        return self.__call__()

    def __call__(self, *args, **kwargs):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }

    def __str__(self):
        return f"Rs(code={self.code}, message={self.message}, data={self.data})"
