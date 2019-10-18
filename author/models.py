from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=108, verbose_name='作者名')
    password = models.CharField(max_length=32, verbose_name='密码')
    introduction = models.CharField(max_length=1000, verbose_name='简介', default='')
    avator = models.ImageField(verbose_name='头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_forbid = models.BooleanField(default=False, verbose_name='是否被禁')
    IDcard = models.CharField(max_length=16, verbose_name='身份证')
    truename = models.CharField(max_length=16, verbose_name='真实姓名')
    email = models.CharField(max_length=50, verbose_name='邮箱', default='')

    class Meta:
        db_table = 'author'
