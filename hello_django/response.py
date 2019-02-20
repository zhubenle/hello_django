# from hello_django.error import BaseError


class Code:
    """状态码"""

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


class Resp:
    """响应对象"""

    def __init__(self):
        self.code = CODE_10000.code
        self.msg = CODE_10000.msg
        self.data = None

    def success(self, data):
        self.data = data
        return self

    def fail(self, code: Code):
        self.code = code.code
        self.msg = code.msg
        return self

    # def fail_error(self, error: BaseError):
    #     self.code = error.code.code
    #     self.msg = error.code.msg
    #     return self


CODE_10000 = Code(10000, 'success')
CODE_10001 = Code(10001, 'parameter can not be empty')
CODE_10002 = Code(10002, 'username can not be found')
CODE_10003 = Code(10002, 'password is error')
CODE_99999 = Code(99999, 'server error')