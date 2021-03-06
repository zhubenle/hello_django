# Generated by Django 2.1.5 on 2019-03-07 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_django', '0004_auto_20190228_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(db_index=True, max_length=32, unique=True, verbose_name='角色名称'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=64, unique=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(db_index=True, max_length=11, unique=True, verbose_name='手机号'),
        ),
    ]
