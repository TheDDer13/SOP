from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from django.db.models.fields import BooleanField, CharField, IntegerField, DateField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField

# Create your models here.
class Regulation(models.Model):
    name = CharField(max_length=225,verbose_name='Tên quy trình')
    code = CharField(max_length=64,verbose_name='Mã quy trình')
    revision = IntegerField(verbose_name='Lần ban hành') #Validate increasing number
    issued_date = DateField(null=True,verbose_name='Ngày ban hành')
    issued_by = ForeignKey(User,on_delete=PROTECT,related_name='department',verbose_name='Phòng ban hành')
    recall = BooleanField(verbose_name='Thu hồi')
    link = URLField(verbose_name='Link tài liệu')
    classified = CharField(max_length=225,verbose_name='Phân loại')
    def __str__(self) -> str:
        return f"{self.code}: {self.name}"

class Permission(models.Model):
    document = OneToOneField(Regulation,on_delete=PROTECT,related_name='doc',primary_key=True)
    user = ManyToManyField(User,related_name='share')
    def __str__(self) -> str:
        return f"{self.document}"