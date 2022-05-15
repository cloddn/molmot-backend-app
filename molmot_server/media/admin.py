from django.contrib import admin

from media import models

# Register your models here.

@admin.register(models.UIPhoto)
class UIPhotoAdmin(admin.ModelAdmin):
    list_display = (
        'field',
        'title',
        'body',
        'uuid',
        'indexnum',
        'photo_file'
    )

@admin.register(models.SmartResultQRPhoto)
class SmartResultQRPhotoAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'member_id',
        'photo_file'
    )