# Generated by Django 2.1.5 on 2019-01-19 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello_django', '0005_auto_20190118_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backend',
            name='id',
            field=models.AutoField(help_text='自增主键', primary_key=True, serialize=False),
        ),
    ]
