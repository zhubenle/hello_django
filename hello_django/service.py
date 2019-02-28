import logging

from django.contrib.sessions.backends.base import SessionBase
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.utils import timezone

from hello_django import utils
from hello_django.backend.vos import MenuVO
from hello_django.costant import SESSION_USER_KEY, SESSION_EXPIRY_TIMES, SESSION_MENUS_KEY
from hello_django.exception import LoginError
from hello_django.response import CODE_10002, CODE_10003
from hello_django.request import LoginRequestParam
from hello_django.backend.models import User, Menu

logger = logging.getLogger(__name__)


class LoginService:
    """登录服务类"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if LoginService.__instance is None:
            LoginService.__instance = super(LoginService, cls).__new__(cls)
        return LoginService.__instance

    def do_login(self, params: LoginRequestParam):
        """
        处理登录
        :param params: 登录请求参数
        :return:
        """
        params.validate()
        request: HttpRequest = params.request
        session: SessionBase = request.session
        try:
            user = User.objects.get(username=params.username, del_status=0)
            user.last_login_ip = request.META.get('REMOTE_ADDR')
            user.last_login_time = timezone.now()
            user.save()
        except ObjectDoesNotExist:
            raise LoginError(CODE_10002)

        if user.password != params.password:
            raise LoginError(CODE_10003)

        logger.info('backend %s login success', user.username)
        menus = Menu.objects.filter(del_status=0, rolemenu__role__userrole__user=user,
                                    rolemenu__role__del_status=0).order_by('-sort')

        session.clear_expired()
        session.set_expiry(SESSION_EXPIRY_TIMES)
        session[SESSION_USER_KEY] = user
        menus_json = utils.objs_to_json(menus, lambda obj: MenuVO(menu=obj))
        session[SESSION_MENUS_KEY] = menus_json
