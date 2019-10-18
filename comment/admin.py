from django.contrib import admin
from .models import Comment
# Register your models here.


class Commentadmin(admin.ModelAdmin):
    list_display = ['created_time']


admin.site.register(Comment,Commentadmin)