import logging
from functools import reduce

from django.core.paginator import Paginator, Page
from django.db.models import Q

from hello_django import utils
from hello_django.backend.models import User, Role, Menu
from hello_django.backend.request import UsersRequestParam, RolesRequestParam, MenusRequestParam
from hello_django.backend.vos import UserVO, RoleVO, MenuVO

logger = logging.getLogger(__name__)


class BdUserService:
    """后台用户服务类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if BdUserService.__instance is None:
            BdUserService.__instance = super(BdUserService, cls).__new__(cls)
        return BdUserService.__instance

    def obtain_page_users(self, params: UsersRequestParam):
        """
        获取用户分页数据
        :param params: 请求参数对象
        :return: 用户分页数据
        """
        users = User.objects.filter(params.get_search_q()).order_by(*params.get_order())
        paginator = Paginator(users, params.page_size)
        return utils.format_page_data(paginator, params, convert_func=lambda obj: UserVO(user=obj))


class BdRoleService:
    """后台角色服务类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if BdRoleService.__instance is None:
            BdRoleService.__instance = super(BdRoleService, cls).__new__(cls)
        return BdRoleService.__instance

    def obtain_page_roles(self, params: RolesRequestParam):
        """
        获取角色分页数据
        :param params: 请求参数对象
        :return: 角色分页数据
        """
        roles = Role.objects.filter(params.get_search_q()).order_by(*params.get_order())
        paginator = Paginator(roles, params.page_size)
        return utils.format_page_data(paginator, params, convert_func=lambda obj: RoleVO(role=obj))


class BdMenuService:
    """后台菜单服务类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if BdMenuService.__instance is None:
            BdMenuService.__instance = super(BdMenuService, cls).__new__(cls)
        return BdMenuService.__instance

    def obtain_page_menus(self, params: MenusRequestParam):
        """
        获取菜单分页数据
        :param params: 请求参数对象
        :return: 菜单分页数据
        """
        menus = Menu.objects.filter(params.get_search_q()).order_by(*params.get_order())
        paginator = Paginator(menus, params.page_size)
        return utils.format_page_data(paginator, params, convert_func=lambda obj: MenuVO(menu=obj))
