from operator import ge
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import uuid

class UserManager(BaseUserManager):    
    
    use_in_migrations = True    

    #일반 유저생성 - 성별값 미포함
    def create_user(self, email, first_name,last_name,birth,gender,password=None):        
         
        user = self.model(            
            email = self.normalize_email(email),            
            first_name =first_name,
            last_name=last_name,
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
            first_name ="-",
            last_name="-",
  
            birth="0000-00-00",
            password=password   
        )
        user.is_staff=True
        user.save(using=self._db)        
        return user 


class User(AbstractBaseUser):    

    objects = UserManager()
    
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