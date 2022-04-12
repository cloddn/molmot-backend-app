from pyexpat import model
from django.db import models
import uuid

from user.models import Member
# Create your models here.


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(
        max_length=50,
        null=False,
        unique=False
    )   
    location=models.CharField(
        max_length=50,
        null=True,
        unique=False,
        blank=True
    )   
    link=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name

class Support(models.Model): 
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
        ('N', '어느쪽도 아님(None)')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    title=models.CharField(
        max_length=50,
        null=False,
        unique=False
    )   
    detail=models.TextField(verbose_name='상세 설명',)
    submit_link=models.URLField(blank=True,null=True,verbose_name='관련 링크',)
    organizer=models.ForeignKey(Organization,verbose_name='주관사',null=True,on_delete=models.CASCADE)
    start_date=models.DateTimeField(verbose_name='시작 날짜')
    end_date=models.DateTimeField(verbose_name='마감 날짜')
    qualifications=models.TextField(verbose_name='지원자격',null=True)
    located_in=models.CharField(verbose_name='지역',max_length=50,null=True,unique=False)
    age=models.IntegerField(verbose_name='나이',null=True)
    gender = models.CharField(verbose_name='성별',blank=True, default='N',max_length=1, choices=GENDERS, null=True)
    number_of_households=models.IntegerField(verbose_name='가구수',null=True)
    income_ratio=models.IntegerField(verbose_name='한국장학재단 기준 소득분위',null=True)

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    organizer_id=models.ForeignKey(Organization,null=True,on_delete=models.CASCADE)
    member_id=models.ForeignKey(Member,null=True,on_delete=models.CASCADE)
