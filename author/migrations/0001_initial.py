# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-09-26 01:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=108, verbose_name='作者名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('introduction', models.CharField(default='', max_length=1000, verbose_name='简介')),
                ('avator', models.ImageField(upload_to='', verbose_name='头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('is_forbid', models.BooleanField(default=False, verbose_name='是否被禁')),
                ('IDcard', models.CharField(max_length=16, verbose_name='身份证')),
                ('truename', models.CharField(max_length=16, verbose_name='真实姓名')),
                ('email', models.CharField(default='', max_length=50, verbose_name='邮箱')),
            ],
            options={
                'db_table': 'author',
            },
        ),
    ]
