
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

    def success(self, data=None):
        self.data = data
        return self

    def fail(self, code: Code):
        self.code = code.code
        self.msg = code.msg
        return self

    def fail_error(self, error):
        self.code = error.code
        self.msg = error.msg
        return self


CODE_10000 = Code(10000, 'success')

CODE_10001 = Code(10001, 'parameter can not be empty')
CODE_10002 = Code(10002, 'username can not be found')
CODE_10003 = Code(10003, 'password is error')
CODE_10004 = Code(10004, 'username invalid format')
CODE_10005 = Code(10005, 'password invalid format')
CODE_10006 = Code(10006, 'real_name invalid format')
CODE_10007 = Code(10007, 'email invalid format')
CODE_10008 = Code(10008, 'phone invalid format')
CODE_10009 = Code(10009, 'role can not be empty')

CODE_10010 = Code(10010, 'User can not be found')
CODE_10011 = Code(10011, 'Role can not be found')
CODE_10012 = Code(10012, 'Menu can not be found')

CODE_99999 = Code(99999, 'server error')