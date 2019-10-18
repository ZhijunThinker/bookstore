from django.db import models
from book.models import Book
from reader.models import Reader_Profile
# Create your models here.


class Bookrack(models.Model):
    book = models.ForeignKey(Book,on_delete='CASCADE')
    reader = models.ForeignKey(Reader_Profile,on_delete='CASCADE')