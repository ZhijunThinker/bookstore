from django.db import models

# Create your models here.
class Reader_Profile(models.Model):
    readername=models.CharField("用户名", max_length=11, primary_key=True)
    nickname=models.CharField("昵称",max_length=30)
    email=models.CharField("邮箱",max_length=50,null=True)
    password=models.CharField("密码",max_length=32)
    sign=models.CharField("个性签名",max_length=50)
    gender=models.CharField("性别",max_length=1)
    avatar=models.ImageField("头像",upload_to='avatar/')
    #charfileld 不要用null,从数据库方面来说可能会影响索引
    class Meta:
        db_table="reader_profile"

