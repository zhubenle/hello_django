from django.http import HttpRequest

from hello_django import utils
from hello_django.exception import ParamError
from hello_django.regex_pattern import PT_PHONE, PT_EMAIL, PT_USERNAME, PT_PASSWORD, PT_REAL_NAME, PT_ROLE_NAME, \
    PT_MENU_TITLE, PT_MENU_URL
from hello_django.request import BaseDataTablesRequestParam
from hello_django.response import CODE_10004, CODE_10005, CODE_10006, CODE_10007, CODE_10008, CODE_10009, CODE_10013, \
    CODE_10018, CODE_10019


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


class RoleRequestParam:
    """角色操作请求参数"""

    def __init__(self, request: HttpRequest):
        self.id: int = request.POST.get(key='id', default=None)
        self.name: str = str.strip(request.POST.get(key='name', default=''))
        self.del_status: bool = utils.str_to_bool(request.POST.get(key='del_status'))
        self.menus: list = request.POST.get(key='menus', default='').split(',')

    def validate(self):
        if not PT_ROLE_NAME.match(self.name):
            raise ParamError(CODE_10013)

    def obtain_dict(self):
        obj_dict = {}
        if self.name:
            obj_dict['name'] = self.name

        if self.del_status is not None:
            obj_dict['del_status'] = self.del_status

        return obj_dict


class MenusRequestParam(BaseDataTablesRequestParam):
    """菜单列表请求参数"""

    def __init__(self, request: HttpRequest):
        super().__init__(request)
        self.id: int = request.POST.get(key='id', default=None)
        self.parent_id: int = request.POST.get(key='parent_id', default=None)
        self.title: str = str.strip(request.POST.get(key='title', default=''))
        self.url: str = str.strip(request.POST.get(key='url', default=''))
        self.icon_class: str = str.strip(request.POST.get(key='icon_class', default=''))
        self.sort: int = request.POST.get(key='sort', default=0)
        self.show: bool = utils.str_to_bool(request.POST.get(key='show'))
        self.del_status: bool = utils.str_to_bool(request.POST.get(key='del_status'))

    def validate(self):
        if not PT_MENU_TITLE.match(self.title):
            raise ParamError(CODE_10018)

        if self.url and not PT_MENU_URL.match(self.url):
            raise ParamError(CODE_10019)

    def obtain_dict(self):
        obj_dict = {}
        if self.parent_id:
            obj_dict['parent_id'] = self.parent_id

        if self.title:
            obj_dict['title'] = self.title

        if self.url:
            obj_dict['url'] = self.url

        if self.icon_class:
            obj_dict['icon_class'] = self.icon_class

        if self.sort:
            obj_dict['sort'] = self.sort

        if self.show is not None:
            obj_dict['show'] = self.show

        if self.del_status is not None:
            obj_dict['del_status'] = self.del_status

        return obj_dict
