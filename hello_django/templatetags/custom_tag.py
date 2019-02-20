import json

from django import template
import datetime

register = template.Library()


@register.filter(name='json_filter_show')
def json_filter_show(value, arg):
    """json字符串过滤指定条件数据"""
    return json.dumps(list(filter(lambda d: d.get('show'), json.loads(value))), ensure_ascii=False)


@register.filter(name='addtwo')
def add_two(value):
    return value + 2


@register.filter
def add_some(value, arg):
    return value + arg


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)
