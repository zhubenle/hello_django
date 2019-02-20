from builtins import dict

from django.http import HttpRequest

from hello_django.error import LoginError
from hello_django.response import CODE_10001


class BaseDataTablesRequestParam:
    """DataTables表格插件请求参数对象"""

    def __init__(self, request: HttpRequest):
        self.request = request
        self.draw = int(request.POST.get(key='draw'))
        self.page_size = int(request.POST.get(key='length', default=10))
        self.page_no = int(request.POST.get(key='start', default=0)) / self.page_size + 1
        self.search_value = request.POST.get(key='search[value]')
        self.search_regex = request.POST.get(key='search[regex]', default=False)
        self.columns = list()
        self.orders = list()
        self.__parse_column_and_order(request)

    def get_order(self):
        """获取组装的排序字段元组"""
        return tuple(map(lambda order: (order.dir.replace('asc', '').replace('desc', '-') +
                                        self.columns[order.column].data), self.orders))

    def get_search(self) -> dict:
        """获取搜索字段元组"""
        search_dict = {}
        for col in self.columns:
            sv: str = col.search_value if col.search_value else self.search_value
            if col.searchable and sv:
                if col.data == 'id':
                    if sv.isdigit():
                        search_dict[col.data] = col.search_value if col.search_value else self.search_value
                else:
                    search_dict[col.data + '__startswith'] = col.search_value if col.search_value else self.search_value
        return search_dict

    def __parse_column_and_order(self, request: HttpRequest):
        """解析列参数"""
        column_index = None
        order_index = None
        column = None
        order = None
        for k, v in request.POST.items():
            k: str = k
            if k.startswith('columns'):
                kl = k.replace('columns[', '').split('][', 1)
                if column_index != kl[0]:
                    column_index = kl[0]
                    column = BaseDataTablesRequestParam.Column()
                    if column:
                        self.columns.append(column)
                setattr(column, kl[1].replace('][', '_').replace(']', ''), v)
            elif k.startswith('order'):
                kl = k.replace('order[', '').split('][', 1)
                if order_index != kl[0]:
                    order_index = kl[0]

                    order = BaseDataTablesRequestParam.Order()
                    if order:
                        self.orders.append(order)
                setattr(order, kl[1].replace(']', ''), v)

    class Column:
        """DataTables表格插件请求列参数对象"""

        data: str = None
        name: str = None
        searchable: bool = None
        orderable: bool = None
        search_value: str = None
        search_regex: bool = None

        def __setattr__(self, key, value):
            if 'true' == value:
                value = True
            elif 'false' == value:
                value = False

            self.__dict__[key] = value

        def __str__(self):
            return 'Column{data=%s, name=%s, searchable=%s, orderable=%s, search_value=%s, search_regex=%s}' \
                   % (self.data, self.name, self.searchable, self.orderable, self.search_value, self.search_regex)

    class Order:
        """DataTables表格插件请求排序参数对象"""

        column: int = None
        dir: str = None

        def __setattr__(self, key, value):
            if 'column' == key:
                value = int(value)
            self.__dict__[key] = value

        def __str__(self):
            return 'Order{column=%s, dir=%s}' % (self.column, self.dir)


class LoginRequestParam:
    """登录请求参数"""

    def __init__(self, request: HttpRequest):
        self.request = request
        self.username = request.POST.get(key='username')
        self.password = request.POST.get(key='password')
        self.remember_me = request.POST.get(key='remember_me', default=False)

    def __str__(self):
        return 'LoginRequestParam{username=%s, password=%s, remember_me=%s}' \
               % (self.username, self.password, self.remember_me)

    def validate(self):
        if not self.username or not self.password:
            raise LoginError(CODE_10001)
