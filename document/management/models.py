from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from django.db.models.fields import CharField, IntegerField, DateField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField

# Create your models here.
class Regulation(models.Model):
    name = CharField(max_length=64)
    code = CharField(max_length=10)
    revision = IntegerField() #Validate increasing number
    issued_date = DateField()
    issued_by = ForeignKey(User,on_delete=PROTECT,related_name='department')
    link = URLField()

class QA(models.Model):
    document = OneToOneField(Regulation,on_delete=PROTECT,related_name='QAdoc',primary_key=True)
    user = ManyToManyField(User,related_name='QAshare')

class QC(models.Model):
    document = OneToOneField(Regulation,on_delete=PROTECT,related_name='QCdoc')
    user = ManyToManyField(User,related_name='QCshare')