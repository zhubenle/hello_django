# Generated by Django 2.1.5 on 2019-02-20 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='自增主键')),
                ('parent_id', models.IntegerField(null=True, verbose_name='父菜单ID')),
                ('title', models.CharField(max_length=64, verbose_name='菜单名称')),
                ('url', models.URLField(null=True, verbose_name='菜单URL')),
                ('icon_class', models.CharField(max_length=64, null=True, verbose_name='菜单图标')),
                ('show', models.BooleanField(default=0, verbose_name='是否显示，1-显示，0-不显示')),
                ('sort', models.IntegerField(default=0, verbose_name='展示排序')),
                ('update_time', models.DateTimeField(verbose_name='更新时间')),
                ('create_time', models.DateTimeField(db_index=True, verbose_name='入库时间')),
                ('del_status', models.BooleanField(default=0, verbose_name='删除状态，1-删除， 0-未删除')),
            ],
            options={
                'verbose_name': '菜单表',
                'verbose_name_plural': '菜单表',
                'db_table': 'menu',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='自增主键')),
                ('name', models.CharField(max_length=32, verbose_name='角色名称')),
                ('update_time', models.DateTimeField(verbose_name='更新时间')),
                ('create_time', models.DateTimeField(db_index=True, verbose_name='入库时间')),
                ('del_status', models.BooleanField(default=0, verbose_name='删除状态，1-删除， 0-未删除')),
            ],
            options={
                'verbose_name': '角色表',
                'verbose_name_plural': '角色表',
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='RoleMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='自增主键')),
                ('update_time', models.DateTimeField(verbose_name='更新时间')),
                ('create_time', models.DateTimeField(db_index=True, verbose_name='入库时间')),
                ('del_status', models.BooleanField(default=0, verbose_name='删除状态，1-删除， 0-未删除')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hello_django.Menu')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hello_django.Role')),
            ],
            options={
                'verbose_name': '角色菜单关联表',
                'verbose_name_plural': '角色菜单关联表',
                'db_table': 'role_menu',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='自增主键')),
                ('username', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('real_name', models.CharField(db_index=True, max_length=20, verbose_name='真实名称')),
                ('email', models.EmailField(db_index=True, max_length=32, verbose_name='邮箱')),
                ('phone', models.CharField(db_index=True, max_length=11, verbose_name='手机号')),
                ('last_login_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='最后登录ip')),
                ('last_login_time', models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间')),
                ('create_time', models.DateTimeField(db_index=True, verbose_name='入库时间')),
                ('del_status', models.BooleanField(default=0, verbose_name='删除状态，1-删除， 0-未删除')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='自增主键')),
                ('update_time', models.DateTimeField(verbose_name='更新时间')),
                ('create_time', models.DateTimeField(db_index=True, verbose_name='入库时间')),
                ('del_status', models.BooleanField(default=0, verbose_name='删除状态，1-删除， 0-未删除')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hello_django.Role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hello_django.User')),
            ],
            options={
                'verbose_name': '用户角色关联表',
                'verbose_name_plural': '用户角色关联表',
                'db_table': 'user_role',
            },
        ),
    ]
