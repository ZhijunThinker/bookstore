from django.db import models
from author.models import Author


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=108, verbose_name='书名')
    introduction = models.CharField(max_length=1000, verbose_name='简介', default='')
    author = models.ForeignKey(Author, on_delete='CASCADE')
    classification = models.IntegerField(verbose_name='分类', default=0)
    image = models.ImageField(verbose_name='头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    is_forbid = models.BooleanField(default=False, verbose_name='是否被禁')
    click_volume = models.IntegerField(default=0, verbose_name='点击量')
    like_volume = models.IntegerField(default=0, verbose_name='点赞量')
    is_end = models.BooleanField(default=False, verbose_name='是否完结')
    word_count = models.IntegerField(verbose_name='字数', default=0)
    collection_amount = models.IntegerField(verbose_name='收藏量', default=0)

    class Meta:
        db_table = 'book'
