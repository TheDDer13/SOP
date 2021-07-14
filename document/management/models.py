from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from django.db.models.fields import BooleanField, CharField, IntegerField, DateField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField

# Create your models here.
class Classification(models.Model):
    classified = models.CharField(max_length=20,verbose_name='Phân loại')
    def __str__(self) -> str:
        return f"{self.classified}"

class SOP(models.Model):
    name = CharField(max_length=225,verbose_name='Tên quy trình')
    code = CharField(max_length=64,verbose_name='Mã quy trình')
    revision = IntegerField(verbose_name='Lần ban hành') #Validate increasing number
    issued_date = DateField(null=True,verbose_name='Ngày ban hành')
    issued_by = ForeignKey(User,on_delete=PROTECT,related_name='department',verbose_name='Phòng ban hành')
    recall = BooleanField(verbose_name='Thu hồi')
    link = URLField(verbose_name='Link tài liệu')
    dept_classified = CharField(max_length=225,verbose_name='Phân loại của Phòng')
    sys_classified = ManyToManyField(Classification,verbose_name='Phân loại của Chất lượng',related_name='sys_classified')
    permission = ManyToManyField(User,verbose_name='Phòng ban tiếp nhận',related_name='share')
    def __str__(self) -> str:
        return f"{self.code}: {self.name}"



