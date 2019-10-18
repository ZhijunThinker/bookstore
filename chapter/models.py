from django.db import models
from book.models import Book
# Create your models here.
class Chapter(models.Model):
    name = models.CharField(max_length=108, verbose_name='章节名')
    book=models.ForeignKey(Book,on_delete='CASCADE')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    content=models.TextField(verbose_name='内容')
    class Meta:
        db_table = 'chapter'