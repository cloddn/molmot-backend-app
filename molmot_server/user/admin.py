from user import models
from django.contrib import admin

# Register your models here.
@admin.register(models.Member)
class Member(admin.ModelAdmin):
     list_display= (
     'pk',
    'email',
    'password',
     'username',
     'nickname',
     'colleage',
     'colleage_locatedin',
     'address',
     'city_address',
     'zipcode',
     'birth',
     'phone_number',
     'age',
     'gender',
     'date_joined',
    'last_login',
    'is_smart_recommed',
    'is_active',
    'privacy_agreement'
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

@admin.register(models.CityAddress)
class CityAddress(admin.ModelAdmin):
     list_display= (
     
    'city',
    'address'
     )


