import logging

from django.contrib.sessions.backends.base import SessionBase
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST

from hello_django.costant import GET, POST
from hello_django.error import LoginError
from hello_django.request import LoginRequestParam
from hello_django.service import LoginService

logger = logging.getLogger(__name__)


def index(request: HttpRequest):
    """首页"""
    return render(request, 'index.html')


@require_http_methods(['GET', 'POST'])
def login(request: HttpRequest):
    """登录"""
    if request.method == GET:
        return render(request, 'login.html')
    if request.method == POST:
        try:
            LoginService().do_login(params=LoginRequestParam(request))
        except LoginError as err:
            logger.warning(err)
            return render(request, 'login.html', {'err': err})

        return HttpResponseRedirect(redirect_to='/index/')


@require_POST
def logout(request: HttpRequest):
    """退出"""
    session: SessionBase = request.session
    session.flush()
    return HttpResponseRedirect(redirect_to='/index/')


def to_error(request, code: str):
    """错误页"""
    return render(request, '{}.html'.format(code))
