from user import models
from django.contrib import admin

# Register your models here.
@admin.register(models.Member)
class Member(admin.ModelAdmin):
     list_display= (
    'email',
    'password',
     'username',
     'nickname',
     'locatedin',
     'address',
     'zipcode',
     'birth',
     'phone_number',
     'age',
     'gender',
     'date_joined',
    'last_login',
    'is_active'
     )


@admin.register(models.AuthSMS)
class AuthSMS(admin.ModelAdmin):
     list_display= (
    'phone_number',
    'auth_number',
     )

@admin.register(models.MemberFCMDevice)
class MemberFCMDevice(admin.ModelAdmin):
     list_display= (
    'last_update',
     )
