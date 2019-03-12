import logging

from django.core.paginator import Paginator
from django.utils import timezone

from hello_django import utils
from hello_django.backend.models import User, Role, Menu, UserRole, RoleMenu
from hello_django.backend.request import UsersRequestParam, RolesRequestParam, MenusRequestParam, UserRequestParam, \
    RoleRequestParam
from hello_django.backend.vos import UserVO, RoleVO, MenuVO
from hello_django.exception import ParamError
from hello_django.response import CODE_10001, CODE_10010, CODE_10011, CODE_10014, CODE_10015, CODE_10016, CODE_10017, \
    CODE_10012, CODE_10021, CODE_10020

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

    def obtain_user(self, params: UserRequestParam):
        """
        获取单个用户
        :param params:
        :return:
        """
        query_dict: dict = params.obtain_dict()
        if params.id:
            query_dict['id'] = params.id
        user = User.objects.filter(**query_dict).first()
        if not user:
            raise ParamError(CODE_10010)
        user_vo = UserVO(user=user)
        roles = Role.objects.filter(del_status=False, userrole__user=user)
        user_vo.roles = utils.objs_to_dicts(roles, lambda obj: RoleVO(role=obj))
        return utils.obj_to_dict(user_vo)

    def add_user(self, params: UserRequestParam):
        """
        添加用户
        :param params:
        :return:
        """
        params.validate()
        self.__validate_unique(params)

        now = timezone.now()
        create_dict: dict = params.obtain_dict()
        create_dict['create_time'] = now
        create_dict['update_time'] = now
        user = User.objects.create(**create_dict)
        user.save()
        # 添加角色关联关系
        for role_id in params.roles:
            UserRole.objects.create(user=user, role_id=role_id, create_time=now)

        return utils.obj_to_dict(user, lambda obj: UserVO(user=obj))

    def update_user(self, params: UserRequestParam):
        """
        更新用户
        :param params:
        :return:
        """
        update_dict: dict = params.obtain_dict()

        if not params.id or not update_dict:
            raise ParamError(CODE_10001)

        self.__validate_unique(params)

        now = timezone.now()
        if params.roles:
            UserRole.objects.filter(user_id=params.id).delete()
            for role_id in params.roles:
                UserRole.objects.create(user_id=params.id, role_id=role_id, create_time=now).save()

        update_dict['update_time'] = now
        return User.objects.filter(id=params.id).update(**update_dict)

    def __validate_unique(self, params: UserRequestParam):
        """唯一参数校验"""
        if User.objects.filter(username=params.username).exclude(id=params.id).exists():
            raise ParamError(CODE_10014)

        if User.objects.filter(email=params.email).exclude(id=params.id).exists():
            raise ParamError(CODE_10015)

        if User.objects.filter(phone=params.phone).exclude(id=params.id).exists():
            raise ParamError(CODE_10016)


class BdRoleService:
    """后台角色服务类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if BdRoleService.__instance is None:
            BdRoleService.__instance = super(BdRoleService, cls).__new__(cls)
        return BdRoleService.__instance

    def obtain_roles(self, params: RoleRequestParam):
        """
        获取所有角色
        :return: 角色列表
        """
        roles = Role.objects.all(**params.obtain_dict())
        return utils.objs_to_dicts(roles, convert_func=lambda obj: RoleVO(role=obj))

    def obtain_page_roles(self, params: RolesRequestParam):
        """
        获取角色分页数据
        :param params: 请求参数对象
        :return: 角色分页数据
        """
        roles = Role.objects.filter(params.get_search_q()).order_by(*params.get_order())
        paginator = Paginator(roles, params.page_size)
        return utils.format_page_data(paginator, params, convert_func=lambda obj: RoleVO(role=obj))

    def obtain_role(self, params: RoleRequestParam):
        """
        获取单个角色
        :param params:
        :return:
        """
        query_dict: dict = params.obtain_dict()
        if params.id:
            query_dict['id'] = params.id
        role = Role.objects.filter(**query_dict).first()
        if not role:
            raise ParamError(CODE_10011)
        role_vo = RoleVO(role=role)
        menus = Menu.objects.filter(del_status=False, rolemenu__role=role)
        role_vo.menus = utils.objs_to_dicts(menus, lambda obj: MenuVO(menu=obj))
        return utils.obj_to_dict(role_vo)

    def add_role(self, params: RoleRequestParam):
        """
        添加角色
        :param params:
        :return:
        """
        params.validate()
        if Role.objects.filter(name=params.name).exists():
            raise ParamError(CODE_10017)

        now = timezone.now()
        create_dict: dict = params.obtain_dict()
        create_dict['create_time'] = now
        create_dict['update_time'] = now
        role = Role.objects.create(**create_dict)
        role.save()
        # 添加菜单关联关系
        for menu_id in params.menus:
            RoleMenu.objects.create(role=role, menu_id=menu_id, create_time=now)

    def update_role(self, params: RoleRequestParam):
        """
        更新角色
        :param params:
        :return:
        """
        update_dict: dict = params.obtain_dict()

        if not params.id or not update_dict:
            raise ParamError(CODE_10001)

        if Role.objects.filter(name=params.name).exclude(id=params.id).exists():
            raise ParamError(CODE_10017)

        now = timezone.now()
        if params.menus:
            RoleMenu.objects.filter(role_id=params.id).delete()
            for menu_id in params.menus:
                RoleMenu.objects.create(role_id=params.id, menu_id=menu_id, create_time=now)
        update_dict['update_time'] = now
        return Role.objects.filter(id=params.id).update(**update_dict)


class BdMenuService:
    """后台菜单服务类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if BdMenuService.__instance is None:
            BdMenuService.__instance = super(BdMenuService, cls).__new__(cls)
        return BdMenuService.__instance

    def obtain_menus(self, params: MenusRequestParam):
        """
        获取所有菜单
        :return: 菜单列表
        """
        menus = Menu.objects.all(**params.obtain_dict())
        return utils.objs_to_dicts(menus, convert_func=lambda obj: MenuVO(menu=obj))

    def obtain_page_menus(self, params: MenusRequestParam):
        """
        获取菜单分页数据
        :param params: 请求参数对象
        :return: 菜单分页数据
        """
        menus = Menu.objects.filter(params.get_search_q()).order_by(*params.get_order())
        paginator = Paginator(menus, params.page_size)
        return utils.format_page_data(paginator, params, convert_func=lambda obj: MenuVO(menu=obj))

    def obtain_menu(self, params: MenusRequestParam):
        """
        获取菜单
        :param params:
        :return:
        """
        query_dict: dict = params.obtain_dict()
        if params.id:
            query_dict['id'] = params.id
        menu = Menu.objects.filter(**query_dict).first()
        if not menu:
            raise ParamError(CODE_10012)

        menu_vo = MenuVO(menu=menu)
        if menu_vo.parent_id:
            pm = Menu.objects.filter(id=menu_vo.parent_id)
            menu_vo.parent_menu = utils.obj_to_dict(pm, lambda obj: MenuVO(menu=obj))

        return utils.obj_to_dict(menu, lambda obj: MenuVO(menu=obj))

    def add_menu(self, params: MenusRequestParam):
        """
        添加菜单
        :param params:
        :return:
        """
        params.validate()
        if Role.objects.filter(name=params.title).exists():
            raise ParamError(CODE_10020)

        if Role.objects.filter(name=params.url).exists():
            raise ParamError(CODE_10021)

        now = timezone.now()
        create_dict: dict = params.obtain_dict()
        create_dict['create_time'] = now
        create_dict['update_time'] = now
        menu = Menu.objects.create(**create_dict)
        menu.save()

    def update_menu(self, params: MenusRequestParam):
        """
        更新菜单
        :param params:
        :return:
        """
        update_dict: dict = params.obtain_dict()

        if not params.id or not update_dict:
            raise ParamError(CODE_10001)

        if Role.objects.filter(name=params.title).exclude(id=params.id).exists():
            raise ParamError(CODE_10020)

        if Role.objects.filter(name=params.url).exclude(id=params.id).exists():
            raise ParamError(CODE_10021)

        now = timezone.now()
        update_dict['update_time'] = now
        return Menu.objects.filter(id=params.id).update(**update_dict)
