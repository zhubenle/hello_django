from django.http import HttpRequest

from hello_django import utils
from hello_django.exception import ParamError
from hello_django.regex_pattern import PT_PHONE, PT_EMAIL, PT_USERNAME, PT_PASSWORD, PT_REAL_NAME
from hello_django.request import BaseDataTablesRequestParam
from hello_django.response import CODE_10004, CODE_10005, CODE_10006, CODE_10007, CODE_10008, CODE_10009


class UsersRequestParam(BaseDataTablesRequestParam):
    """用户列表请求参数"""

    def __init__(self, request: HttpRequest):
        super().__init__(request)


class UserRequestParam:
    """用户操作请求参数"""

    def __init__(self, request: HttpRequest):
        self.id: int = request.POST.get(key='id', default=None)
        self.username: str = str.strip(request.POST.get(key='username', default=''))
        self.password: str = str.strip(request.POST.get(key='password', default=''))
        self.real_name: str = str.strip(request.POST.get(key='real_name', default=''))
        self.email: str = str.strip(request.POST.get(key='email', default=''))
        self.phone: str = str.strip(request.POST.get(key='phone', default=''))
        self.del_status: bool = utils.str_to_bool(request.POST.get(key='del_status'))
        self.roles: list = request.POST.get(key='roles', default='').split(',')

    def validate(self):
        if not PT_USERNAME.match(self.username):
            raise ParamError(CODE_10004)

        if not PT_PASSWORD.match(self.password):
            raise ParamError(CODE_10005)

        if not PT_REAL_NAME.match(self.real_name):
            raise ParamError(CODE_10006)

        if not PT_EMAIL.match(self.email) or len(self.email) > 64:
            raise ParamError(CODE_10007)

        if not PT_PHONE.match(self.phone):
            raise ParamError(CODE_10008)

        if not self.roles:
            raise ParamError(CODE_10009)

    def obtain_dict(self):
        obj_dict = {}
        if self.username:
            obj_dict['username'] = self.username

        if self.password:
            obj_dict['password'] = self.password

        if self.real_name:
            obj_dict['real_name'] = self.real_name

        if self.email:
            obj_dict['email'] = self.email

        if self.phone:
            obj_dict['phone'] = self.phone

        if self.del_status is not None:
            obj_dict['del_status'] = self.del_status

        return obj_dict


class RolesRequestParam(BaseDataTablesRequestParam):
    """角色列表请求参数"""

    def __init__(self, request: HttpRequest):
        super().__init__(request)


class MenusRequestParam(BaseDataTablesRequestParam):
    """菜单列表请求参数"""

    def __init__(self, request: HttpRequest):
        super().__init__(request)
