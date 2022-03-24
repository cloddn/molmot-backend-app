from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid


class User(AbstractBaseUser):    
    
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
  
    gender = models.CharField(verbose_name='gender',blank=True, default='N',max_length=1, choices=GENDERS, null=True)
    birth = models.CharField(verbose_name='birth', max_length=10,null=True,blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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