import logging

from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from hello_django import utils
from hello_django.backend.request import UsersRequestParam, RolesRequestParam, MenusRequestParam, UserRequestParam, \
    RoleRequestParam
from hello_django.backend.service import BdUserService, BdRoleService, BdMenuService
from hello_django.exception import BaseError
from hello_django.response import Resp, CODE_99999
from hello_django.utils import CustomerEncoder

logger = logging.getLogger(__name__)


@require_GET
def to_profile(request: HttpRequest):
    """个人信息页面"""
    user = BdUserService().obtain_user(params=UserRequestParam(request))
    return render(request, 'backend/profile.html', context={'user': user})


# ----------用户部分------------
@require_GET
def to_users(request):
    """用户列表页"""
    return render(request, 'backend/users.html')


@require_POST
def ajax_obtain_page_users(request: HttpRequest):
    """获取用户分页列表数据"""
    resp = Resp()
    try:
        result = BdUserService().obtain_page_users(params=UsersRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('obtain page users fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('obtain page users error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_obtain_user(request: HttpRequest):
    """获取单个用户数据"""
    resp = Resp()
    try:
        result = BdUserService().obtain_user(params=UserRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('obtain user fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('obtain user error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_add_user(request: HttpRequest):
    """添加用户"""
    resp = Resp()
    try:
        result = BdUserService().add_user(params=UserRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('add user fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('add user error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_update_user(request: HttpRequest):
    """更新用户"""
    resp = Resp()
    try:
        result = BdUserService().update_user(params=UserRequestParam(request))
        resp.success(result)
    except BaseError as e:
        logger.error('update user fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('update user error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


# ----------角色部分------------
@require_GET
def to_roles(request: HttpRequest):
    """角色列表页"""
    return render(request, 'backend/roles.html')


@require_POST
def ajax_obtain_all_roles(request: HttpRequest):
    """获取所有角色数据"""
    resp = Resp()
    try:
        result = BdRoleService().obtain_roles()
        resp.success(data=result)
    except BaseError as e:
        logger.error('obtain all roles fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('obtain all roles error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_obtain_page_roles(request: HttpRequest):
    """获取角色分页数据"""
    resp = Resp()
    try:
        result = BdRoleService().obtain_page_roles(params=RolesRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('obtain page roles fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('obtain page roles error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_obtain_role(request: HttpRequest):
    """获取单个角色"""
    resp = Resp()
    try:
        result = BdRoleService().obtain_role(params=RoleRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('obtain role fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('obtain role error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_add_role(request: HttpRequest):
    """添加角色"""
    resp = Resp()
    try:
        result = BdRoleService().add_role(params=RoleRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('add role fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('add role error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_update_role(request: HttpRequest):
    """更新角色"""
    resp = Resp()
    try:
        result = BdRoleService().update_role(params=RoleRequestParam(request))
        resp.success(result)
    except BaseError as e:
        logger.error('update role fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('update role error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


# ----------菜单部分----------
@require_GET
def to_menus(request: HttpRequest):
    """菜单列表页"""
    return render(request, 'backend/menus.html')


@require_POST
def ajax_obtain_all_menus(request: HttpRequest):
    """获取所有菜单"""
    resp = Resp()
    try:
        result = BdMenuService().obtain_all_menus()
        resp.success(data=result)
    except BaseError as e:
        logger.error('obtain all menus fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('obtain all menus error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_obtain_page_menus(request: HttpRequest):
    """获取菜单分页数据"""
    resp = Resp()
    try:
        result = BdMenuService().obtain_page_menus(params=MenusRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('obtain page menus fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('obtain page menus error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_obtain_menu(request: HttpRequest):
    """获取单个菜单"""
    resp = Resp()
    try:
        result = BdMenuService().obtain_menu(params=MenusRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('obtain menu fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('obtain menu error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_add_menu(request: HttpRequest):
    """添加菜单"""
    resp = Resp()
    try:
        result = BdMenuService().add_menu(params=MenusRequestParam(request))
        resp.success(data=result)
    except BaseError as e:
        logger.error('add menu fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('add menu error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)


@require_POST
def ajax_update_menu(request: HttpRequest):
    """更新菜单"""
    resp = Resp()
    try:
        result = BdMenuService().update_menu(params=MenusRequestParam(request))
        resp.success(result)
    except BaseError as e:
        logger.error('update menu fail: %s', e)
        resp.fail_error(e)
    except Exception as e:
        logger.error('update menu error: %s', e)
        resp.fail(CODE_99999)
    return JsonResponse(utils.obj_to_dict(resp), encoder=CustomerEncoder)
