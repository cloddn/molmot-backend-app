from user import models
from django.contrib import admin

# Register your models here.
@admin.register(models.Member)
class Member(admin.ModelAdmin):
     list_display= (
    'email',
    'password',
     'username',
     'birth',
     'age',
     'gender',
     'date_joined',
    'last_login',
    'is_active'
     )
