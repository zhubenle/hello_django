import logging

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from hello_django import utils
from hello_django.backend.request import UsersRequestParam, RolesRequestParam, MenusRequestParam
from hello_django.backend.service import BdUserService, BdRoleService, BdMenuService
from hello_django.error import BaseError
from hello_django.response import Resp, CODE_99999
from hello_django.utils import CustomerEncoder
from .models import User

logger = logging.getLogger(__name__)


@require_GET
def to_profile(request):
    """个人信息页面"""
    user = User.objects.get(id=request.GET.get('id'))
    return render(request, 'backend/profile.html', context={'user': user})


@require_GET
def to_users(request):
    """用户列表页"""
    return render(request, 'backend/users.html')


@require_POST
def ajax_obtain_users(request):
    """获取用户分页列表数据"""
    resp = Resp()
    try:
        result = BdUserService().obtain_page_users(params=UsersRequestParam(request))
        resp.success(data=result)
    except Exception as e:
        logger.error('obtain page user error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_GET
def to_roles(request):
    """用户列表页"""
    return render(request, 'backend/roles.html')


@require_POST
def ajax_obtain_roles(request):
    """获取角色分页列表数据"""
    resp = Resp()
    try:
        result = BdRoleService().obtain_page_roles(params=RolesRequestParam(request))
        resp.success(data=result)
    except Exception as e:
        logger.error('obtain page role error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_GET
def to_menus(request):
    """用户列表页"""
    return render(request, 'backend/menus.html')


@require_POST
def ajax_obtain_menus(request):
    """获取菜单分页列表数据"""
    resp = Resp()
    try:
        result = BdMenuService().obtain_page_menus(params=MenusRequestParam(request))
        resp.success(data=result)
    except Exception as e:
        logger.error('obtain page menu error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)
