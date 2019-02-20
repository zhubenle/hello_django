from hello_django.response import Code


class BaseError(Exception):
    """异常基类"""

    def __int__(self, code: Code):
        self.code = code

    def __str__(self):
        return 'BaseError code=%d, msg=%s' % (self.code.code, self.code.msg)


class LoginError(BaseError):
    """登录异常"""

    def __init__(self, code: Code):
        super().__int__(code)

    def __str__(self):
        return 'LoginError code=%d, msg=%s' % (self.code.code, self.code.msg)