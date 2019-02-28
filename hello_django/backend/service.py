import logging

from django.core.paginator import Paginator
from django.utils import timezone

from hello_django import utils
from hello_django.backend.models import User, Role, Menu, UserRole
from hello_django.backend.request import UsersRequestParam, RolesRequestParam, MenusRequestParam, UserRequestParam
from hello_django.backend.vos import UserVO, RoleVO, MenuVO
from hello_django.exception import ParamError
from hello_django.response import CODE_10001

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

    def obtain_user(self, **kwargs):
        """
        获取单个用户
        :param kwargs:
        :return:
        """
        user = User.objects.filter(**kwargs).first()
        return UserVO(user=user) if not user else None

    def add_user(self, params: UserRequestParam):
        """
        添加用户
        :param params:
        :return:
        """
        params.validate()
        now = timezone.now()
        create_dict: dict = params.obtain_dict()
        create_dict['create_time'] = now
        create_dict['update_time'] = now
        user = User.objects.create(**create_dict)
        user.save()
        # 添加角色
        for role_id in params.roles:
            UserRole.objects.create(user=user, role_id=role_id, create_time=now)

    def update_user(self, params: UserRequestParam):
        """
        更新用户
        :param params:
        :return:
        """
        update_dict: dict = params.obtain_dict()

        if not params.id or len(update_dict) < 1:
            raise ParamError(CODE_10001)

        now = timezone.now()
        if params.roles:
            UserRole.objects.filter(user_id=params.id).delete()
            for role_id in params.roles:
                UserRole.objects.create(user_id=params.id, role_id=role_id, create_time=now).save()

        update_dict['update_time'] = now
        return User.objects.filter(id=params.id).update(**update_dict)


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

    def obtain_all_roles(self):
        """
        获取所有角色
        :return:
        """
        roles = Role.objects.all()
        return map(lambda obj: RoleVO(role=obj), roles)


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
