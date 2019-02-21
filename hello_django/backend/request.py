from django.http import HttpRequest

from hello_django.request import BaseDataTablesRequestParam


class UsersRequestParam(BaseDataTablesRequestParam):
    """用户列表请求参数"""

    def __init__(self, request: HttpRequest):
        super().__init__(request)


class RolesRequestParam(BaseDataTablesRequestParam):
    """角色列表请求参数"""

    def __init__(self, request: HttpRequest):
        super().__init__(request)


class MenusRequestParam(BaseDataTablesRequestParam):
    """菜单列表请求参数"""

    def __init__(self, request: HttpRequest):
        super().__init__(request)
