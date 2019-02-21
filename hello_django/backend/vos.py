class UserVO:
    """管理用户VO对象"""

    def __init__(self, **kwargs):
        user = kwargs.get('user')
        self.id = user.id if user else kwargs.get('id')
        self.username = user.username if user else kwargs.get('username')
        self.password = user.password if user else kwargs.get('password')
        self.real_name = user.real_name if user else kwargs.get('real_name')
        self.email = user.email if user else kwargs.get('email')
        self.phone = user.phone if user else kwargs.get('phone')
        self.last_login_ip = user.last_login_ip if user else kwargs.get('last_login_ip')
        self.last_login_time = user.last_login_time if user else kwargs.get('last_login_time')
        self.update_time = user.update_time if user else kwargs.get('update_time')
        self.create_time = user.create_time if user else kwargs.get('create_time')
        self.del_status = user.del_status if user else kwargs.get('del_status')

    def __str__(self):
        return 'UserVO{{id={}, username={}, real_name={}, email={}, phone={}, last_login_ip={}, ' \
               'last_login_time={}, update_time={}, create_time={}, del_status={}}}' \
            .format(self.id, self.username, self.real_name, self.email, self.phone, self.last_login_ip,
                    self.last_login_time, self.update_time, self.create_time, self.del_status)


class RoleVO:
    """角色VO对象"""

    def __init__(self, **kwargs):
        role = kwargs.get('role')
        self.id = role.id if role else kwargs.get('id')
        self.name = role.name if role else kwargs.get('name')
        self.update_time = role.update_time if role else kwargs.get('update_time')
        self.create_time = role.create_time if role else kwargs.get('create_time')
        self.del_status = role.del_status if role else kwargs.get('del_status')

    def __str__(self):
        return 'RoleVO{{id={}, name={}, update_time={}, create_time={}, del_status={}}}' \
            .format(self.id, self.name, self.update_time, self.create_time, self.del_status)


class MenuVO:
    """菜单VO对象"""

    def __init__(self, **kwargs):
        menu = kwargs.get('menu')
        self.id = menu.id if menu else kwargs.get('id')
        self.parent_id = menu.parent_id if menu else kwargs.get('parent_id')
        self.title = menu.title if menu else kwargs.get('title')
        self.url = menu.url if menu else kwargs.get('url')
        self.icon_class = menu.icon_class if menu else kwargs.get('icon_class')
        self.show = menu.show if menu else kwargs.get('show')
        self.sort = menu.sort if menu else kwargs.get('sort')
        self.update_time = menu.update_time if menu else kwargs.get('update_time')
        self.create_time = menu.create_time if menu else kwargs.get('create_time')
        self.del_status = menu.del_status if menu else kwargs.get('del_status')

    def __str__(self):
        return 'MenuVO{{id={}, parent_id={}, title={}, url={}, icon_class={}, show={}}}' \
            .format(self.id, self.parent_id, self.title, self.url, self.icon_class, self.show)
