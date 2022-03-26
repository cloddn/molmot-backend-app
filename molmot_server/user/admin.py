from user import models
from django.contrib import admin

# Register your models here.
@admin.register(models.User)
class User(admin.ModelAdmin):
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
