from django.http import HttpRequest

from hello_django.request import BaseDataTablesRequestParam


class UsersRequestParam(BaseDataTablesRequestParam):
    """登录请求参数"""

    def __init__(self, request: HttpRequest):
        super().__init__(request)

