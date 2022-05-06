from datetime import datetime
from operator import ge
from os import access
from xxlimited import Null
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import uuid
import hmac
import base64
import hashlib
import json
import requests
from random import randint
import time
from fcm_django.models import AbstractFCMDevice

class MemberManager(BaseUserManager):    
    
    use_in_migrations = True    

    #일반 유저생성 - 성별값 미포함
    def create_user(self, email, username,birth,gender,password=None):        
         
        user = self.model(            
            email = self.normalize_email(email),            
            username=username,
            birth=birth,
            gender=gender
        )
        user.set_password(password)        
        user.save(using=self._db)        
        return user
    #슈퍼유저 생성  - 관리자페이지 게정
    def create_superuser(self, email,password ):        
       
        user = self.create_user(            
            email = self.normalize_email(email),            
            username ="-",

            gender="N",
            birth="0000-00-00",
            password=password   
        )
        user.is_staff=True
        user.save(using=self._db)        
        return user 


class Member(AbstractBaseUser):    

    objects = MemberManager()
    
    email = models.EmailField(        
        max_length=255,  
        null=True,      
        unique=True,    
    )    
    username = models.CharField(
        max_length=50,
        null=False,
        unique=False
    )   
    nickname=models.CharField(
        max_length=50,
        null=True,
        blank=True,
        unique=True
    )   
    #생년월일에 맞춰서 자동기입
    age = models.IntegerField(
        null=True,
        blank=True
    )  
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
        ('N', '어느쪽도 아님(None)')
    )
    colleage=models.CharField(verbose_name='학교', max_length=255,null=True,blank=True)
    colleage_locatedin=models.CharField(verbose_name='소재지', max_length=255,null=True,blank=True)
    address=models.CharField(verbose_name='실거주지', max_length=255,null=True,blank=True)
    city_address=models.CharField(verbose_name='시/군/구', max_length=255,null=True,blank=True)
    zipcode=models.CharField(verbose_name='우편번호', max_length=10,null=True,blank=True)
    gender = models.CharField(verbose_name='성별',blank=True, default='N',max_length=1, choices=GENDERS, null=True)
    birth = models.CharField(verbose_name='생일', max_length=10,null=True,blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number=models.CharField(verbose_name='휴대폰 번호',blank=False,null=True,max_length=11)
    date_joined = models.DateTimeField(auto_now_add=True)  
    is_staff=models.BooleanField(('staff status'),default=False) 
    USERNAME_FIELD = 'email' 
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    #admin page 접근 권한
    def has_module_perms(self, app_label):
        return  True


class TimeStampedModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AuthSMS(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    class Meta:
        db_table = 'auth'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)
        self.send_sms() # 인증번호가 담긴 SMS를 전송

    def	make_signature():
        timestamp = int(time.time() * 1000)
        timestamp = str(timestamp)

        access_key = "B2l9gOSvaNIHnm3Ythaj"	        
        secret_key = "ZRfEfXw0dcL1MLCh3m1DatsJpGI70BYzrtwIp9Z7"	        
        secret_key = bytes(secret_key, 'UTF-8')

        method = "POST"                
        uri = "/sms/v2/services/ncp:sms:kr:283100362786:molmot_app/messages"  
                    # /sms/v2/services/{serviceId}/messages 문자 서비스 같은 경우 com 뒤에서 부터 끝까지 넣어준다.
                    # serviceId는 사용하려는 API의 ServiceID를 넣어준다. 아래 사진 참조
        message = method + " " + uri + "\n" + timestamp + "\n"+ access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        print(signingKey)
        return signingKey

    def send_sms(self):
        service_id = 'ncp:sms:kr:283100362786:molmot_app'
        url = 'https://sens.apigw.ntruss.com'
        uri = '/sms/v2/services/' + service_id + '/messages'
        api_url = url + uri

        body = {
            "type": "SMS",
            "contentType": "COMM",
            "from": "01024494849",
            "content": "[테스트] 인증 번호 [{}]를 입력해주세요.".format(self.auth_number),
            "messages":[{"to":self.phone_number}]
        }
        body2=json.dumps(body)
        timeStamp = str(int(time.time() * 1000))
        access_key="B2l9gOSvaNIHnm3Ythaj"
        signature = AuthSMS.make_signature()

        headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-timestamp": timeStamp,
        "x-ncp-apigw-signature-v2": signature,
        }
        print(api_url)
        result=requests.post(api_url,headers=headers,data=body2)
        print(result.json())

        

    def check_auth_number(self,p_num,a_num):
        if (self.auth_number==int(a_num)):
            return True
        else:
            return False


class MemberFCMDevice(AbstractFCMDevice):
    last_update = models.DateTimeField(auto_now_add=True)  
    

class CityAddress(models.Model):
    
    city=models.CharField(max_length=255,null=True) #특별시,광역시
    address=models.CharField(max_length=255,null=True,unique=True) #행정구