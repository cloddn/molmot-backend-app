from user import models
from django.contrib import admin

# Register your models here.
@admin.register(models.User)
class User(admin.ModelAdmin):
     list_display= (
    'uuid',
    'email',
    'password',
     'name',
     'birth',
     'age',
     'gender',
     'date_joined',
    'last_login',
    'is_active'
     )