import json
from datetime import date, datetime, time

from django.core.paginator import Paginator, Page


class CustomerEncoder(json.JSONEncoder):
    """自定义json编码器"""

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, time):
            return o.strftime('%H:%M:%S')
        else:
            return super().default(o)


def obj_to_dict(obj, convert_func=None):
    """
    对象转字典对象
    :param obj: 对象
    :param convert_func: 转换函数
    :return: 字典
    """
    d = {}
    if not convert_func:
        d.update(obj.__dict__)
    else:
        d.update(convert_func(obj).__dict__)
    return d


def objs_to_dicts(objs, convert_func=None):
    """
    对象列表转字典列
    :param objs: 对象列表
    :param convert_func: 转换函数
    :return: 字典列表
    """
    ds = []
    for obj in objs:
        d = {}
        if not convert_func:
            d.update(obj.__dict__)
        else:
            d.update(convert_func(obj).__dict__)
        ds.append(d)
    return ds


def dict_to_obj(d: dict, obj: object, dict_obj_key_map: dict = None):
    """
    字典值转对象属性
    :param d: 字典
    :param obj: 对象
    :param dict_obj_key_map: 字典字段和对象属性名称对应关系
    :return: 赋值后的对象
    """
    for it in d.items():
        key = it[0]
        val = it[1]
        if dict_obj_key_map and dict_obj_key_map.get(key):
            key = dict_obj_key_map.get(key)
        if hasattr(obj, key):
            setattr(obj, key, val)
    return obj


def to_json(obj):
    """
    序列化对象转json
    :param obj: 对象
    :return: json字符串
    """
    return json.dumps(obj, ensure_ascii=False, cls=CustomerEncoder)


def obj_to_json(obj, convert_func=None):
    """
    非序列化对象转json字符串
    :param obj: 对象
    :param convert_func: 转换函数
    :return: json字符串
    """
    return json.dumps(obj_to_dict(obj, convert_func), ensure_ascii=False, cls=CustomerEncoder)


def objs_to_json(objs, convert_func=None):
    """
    非序列化对象列表转json字符串
    :param objs: 对象列表
    :param convert_func: 转换函数
    :return: json字符串
    """
    return json.dumps(objs_to_dicts(objs, convert_func), ensure_ascii=False, cls=CustomerEncoder)


bool_dict = {'true': True, 'false': False, 'True': True, 'False': False}


def str_to_bool(val: str):
    return bool_dict.get(val, val)


def format_page_data(paginator: Paginator, params, convert_func=None):
    """
    将数据格式化符合DataTables前端插件分页的格式
    :param paginator: Django分页对象
    :param params: 页面插件请求参数
    :param convert_func: 转换函数
    :return: 字典对象
    """
    page: Page = paginator.get_page(params.page_no)
    obj_dict = objs_to_dicts(page.object_list, convert_func=convert_func)
    result = {'draw': params.draw, 'recordsTotal': paginator.count, 'recordsFiltered': paginator.count,
              'data': obj_dict}
    return result
