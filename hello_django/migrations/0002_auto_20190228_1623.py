# Generated by Django 2.1.5 on 2019-02-28 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello_django', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rolemenu',
            name='del_status',
        ),
        migrations.RemoveField(
            model_name='userrole',
            name='del_status',
        ),
    ]
