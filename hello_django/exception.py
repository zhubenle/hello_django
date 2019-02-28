from hello_django.response import Code


class BaseError(Exception):
    """异常基类"""

    def __int__(self, code: Code):
        self.code = code.code
        self.msg = code.msg
        super().__init__()

    def __str__(self):
        return 'code=%d, msg=%s' % (self.code, self.msg)


class LoginError(BaseError):
    """登录异常"""

    def __init__(self, code: Code):
        super().__int__(code)

    def __str__(self):
        return 'LoginError [%s]' % (super().__str__())


class ParamError(BaseError):
    """参数错误异常"""

    def __init__(self, code: Code):
        super().__int__(code)

    def __str__(self):
        return 'ParamError [%s]' % (super().__str__())
