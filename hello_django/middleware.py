import json

from django.contrib.sessions.backends.base import SessionBase
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError

from hello_django import utils
from hello_django.backend.models import User
from hello_django.backend.vos import MenuVO
from hello_django.costant import SESSION_MENUS_KEY, SESSION_USER_KEY, SESSION_SELECT_URL_KEY


class LoginMiddleware:
    """登录拦截中间件"""

    def __init__(self, get_response):
        self.get_response = get_response
        self.not_intercept_urls = ['/logout/', '/index/', '/404/', '/500/', '/403/']

    def __call__(self, request: HttpRequest):
        session: SessionBase = request.session
        session_user: User = session.get(SESSION_USER_KEY)
        path = request.path
        try:
            return self.__auth(path, session_user, session, request)
        except Exception as e:
            if session_user is not None:
                if isinstance(e, PermissionDenied):
                    return HttpResponseRedirect(redirect_to='/403/')

                return HttpResponseRedirect(redirect_to='/500/')
            else:
                return HttpResponseRedirect(redirect_to='/index/')

    def __auth(self, path: str, session_user: User, session: SessionBase, request: HttpRequest):
        """
        权限验证
        :param session: 会话
        :param request: 请求对象
        :return:
        """
        if path != '/login/':
            if session_user is not None:
                # 权限判断
                if self.not_intercept_urls.count(path) > 0:
                    if path == '/index/':
                        session[SESSION_SELECT_URL_KEY] = '/index/'

                    return self.get_response(request)

                menus_json = session.get(SESSION_MENUS_KEY)
                menu_vos = json.loads(menus_json, object_hook=lambda d: utils.dict_to_obj(d, MenuVO()))
                for menu_vo in menu_vos:
                    if menu_vo.url and menu_vo.url == path:
                        session[SESSION_SELECT_URL_KEY] = path
                        return self.get_response(request)
                else:
                    session[SESSION_SELECT_URL_KEY] = '/index/'

                raise PermissionDenied
            else:
                return HttpResponseRedirect(redirect_to='/login/')
        elif session_user is not None:
            return HttpResponseRedirect(redirect_to='/index/')
        else:
            return self.get_response(request)
