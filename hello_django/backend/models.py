from django.db import models


class User(models.Model):
    id = models.AutoField(verbose_name='自增主键', primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=20, unique=True, db_index=True)
    password = models.CharField(verbose_name='密码', max_length=256)
    real_name = models.CharField(verbose_name='真实名称', max_length=20, db_index=True)
    email = models.EmailField(verbose_name='邮箱', max_length=32, db_index=True)
    phone = models.CharField(verbose_name='手机号', max_length=11, db_index=True)
    last_login_ip = models.GenericIPAddressField(verbose_name='最后登录ip', null=True, blank=True)
    last_login_time = models.DateTimeField(verbose_name='最后登录时间', null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间')
    create_time = models.DateTimeField(verbose_name='入库时间', db_index=True)
    del_status = models.BooleanField(verbose_name='删除状态，1-删除， 0-未删除', default=0)

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = '用户表'

    def __str__(self):
        return 'User{{id={}, username={}, real_name={}, email={}, phone={}, last_login_ip={}, ' \
               'last_login_time={}, update_time={}, create_time={}, del_status={}}}' \
            .format(self.id, self.username, self.real_name, self.email, self.phone, self.last_login_ip,
                    self.last_login_time, self.update_time, self.create_time, self.del_status)


class Role(models.Model):
    id = models.AutoField(verbose_name='自增主键', primary_key=True)
    name = models.CharField(verbose_name='角色名称', max_length=32)
    update_time = models.DateTimeField(verbose_name='更新时间')
    create_time = models.DateTimeField(verbose_name='入库时间', db_index=True)
    del_status = models.BooleanField(verbose_name='删除状态，1-删除， 0-未删除', default=0)

    class Meta:
        db_table = 'role'
        verbose_name = '角色表'
        verbose_name_plural = '角色表'

    def __str__(self):
        return 'Role{{id={}, name={}, update_time={}, create_time={}, del_status={}}}' \
            .format(self.id, self.name, self.update_time, self.create_time, self.del_status)


class Menu(models.Model):
    id = models.AutoField(verbose_name='自增主键', primary_key=True)
    parent_id = models.IntegerField(verbose_name='父菜单ID', null=True)
    title = models.CharField(verbose_name='菜单名称', max_length=64)
    url = models.URLField(verbose_name='菜单URL', null=True)
    icon_class = models.CharField(verbose_name='菜单图标', max_length=64, null=True)
    show = models.BooleanField(verbose_name='是否显示，1-显示，0-不显示', default=0)
    sort = models.IntegerField(verbose_name='展示排序', default=0)
    update_time = models.DateTimeField(verbose_name='更新时间')
    create_time = models.DateTimeField(verbose_name='入库时间', db_index=True)
    del_status = models.BooleanField(verbose_name='删除状态，1-删除， 0-未删除', default=0)

    class Meta:
        db_table = 'menu'
        verbose_name = '菜单表'
        verbose_name_plural = '菜单表'

    def __str__(self):
        return 'Menu{{id={}, parent_id={}, title={}, url={}, icon_class={}, show={}, update_time={}, ' \
               'create_time={}, del_status={}}}' \
            .format(self.id, self.parent_id, self.title,
                    self.url, self.icon_class, self.show, self.update_time, self.create_time, self.del_status)


class UserRole(models.Model):
    id = models.AutoField(verbose_name='自增主键', primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(to=Role, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(verbose_name='入库时间', db_index=True)

    class Meta:
        db_table = 'user_role'
        verbose_name = '用户角色关联表'
        verbose_name_plural = '用户角色关联表'


class RoleMenu(models.Model):
    id = models.AutoField(verbose_name='自增主键', primary_key=True)
    role = models.ForeignKey(to=Role, on_delete=models.DO_NOTHING)
    menu = models.ForeignKey(to=Menu, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(verbose_name='入库时间', db_index=True)

    class Meta:
        db_table = 'role_menu'
        verbose_name = '角色菜单关联表'
        verbose_name_plural = '角色菜单关联表'
