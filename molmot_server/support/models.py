from pyexpat import model
from django.db import models
import uuid
from fcm_django.models import FCMDevice

from user.models import Member
# Create your models here.
from django_celery_beat.models import CrontabSchedule, PeriodicTask

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

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    title=models.CharField(
        max_length=50,
        null=False,
        unique=False
    )   
    detail=models.TextField(verbose_name='상세 설명',)
    submit_link=models.URLField(blank=True,null=True,verbose_name='관련 링크',)
    organizer=models.CharField(
        verbose_name='주관사',
        max_length=50,
        null=True
    )
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
    organizer_id=models.ForeignKey(Organization,verbose_name='관심있는 분야',null=True,on_delete=models.CASCADE)
    member_id=models.ForeignKey(Member,null=True,on_delete=models.CASCADE)

class Channel(models.Model):
    channel_name=models.CharField(verbose_name='구독할 채널 작명',max_length=50,null=True,unique=True)
    organizer_id=models.ForeignKey(Organization,verbose_name='관련 제도',null=True,on_delete=models.CASCADE)
    member_id=models.ForeignKey(Member,null=True,on_delete=models.CASCADE)



class SupportNotification(models.Model):
    
    organizer_id=models.ForeignKey(Organization,verbose_name='관심있는 분야',null=True,on_delete=models.CASCADE)
    user_device_info=models.ForeignKey(FCMDevice,verbose_name='유저 디바이스 정보',null=True,on_delete=models.CASCADE)
    last_logined=models.DateTimeField(auto_now=True) #가장 마지막에 로그인한 시간
    sched_noti=models.ForeignKey(PeriodicTask,verbose_name='예정되어있는 알림',null=True,on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("SupportNotification")