from django.db import models
from reader.models import Reader_Profile
from book.models import Book


# Create your models here.
class Comment(models.Model):
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book,on_delete='CASCADE')
    reader = models.ForeignKey(Reader_Profile,on_delete='CASCADE',related_name='评论者')


    class Meta:
        db_table = 'comment'