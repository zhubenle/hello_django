import logging
from functools import reduce

from django.core.paginator import Paginator, Page
from django.db.models import Q

from hello_django import utils
from hello_django.backend.models import User
from hello_django.backend.request import UsersRequestParam
from hello_django.backend.vos import UserVO
from hello_django.response import Resp

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

        q = reduce(lambda q1, q2: q1 | q2, [Q(**{it[0]: it[1]}) for it in params.get_search().items()], Q())
        # q = reduce(lambda q1, q2: q1 | q2,
        #            map(lambda d: Q(**d), map(lambda it: {it[0]: it[1]}, params.get_search().items())), Q())
        print(q)
        users = User.objects.filter(q).order_by(*params.get_order())
        paginator = Paginator(users, params.page_size)
        return utils.format_page_data(paginator, params, convert_func=lambda obj: UserVO(user=obj))


class BdRoleService:
    """后台角色服务类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if BdRoleService.__instance is None:
            BdRoleService.__instance = super(BdRoleService, cls).__new__(cls)
        return BdRoleService.__instance


class BdMenuService:
    """后台菜单服务类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if BdMenuService.__instance is None:
            BdMenuService.__instance = super(BdMenuService, cls).__new__(cls)
        return BdMenuService.__instance
