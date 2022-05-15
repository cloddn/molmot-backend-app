from support import models
from django.contrib import admin

# Register your models here.
@admin.register(models.Organization)
class Organization(admin.ModelAdmin):
     list_display= (
     'uuid',
    'name',
     'location',
     'link'
     )


@admin.register(models.Support)
class Support(admin.ModelAdmin):
     list_display= (
     'uuid',
     'bizId',
    'title',
     'detail',
     'submit_link',
     'organizer',
     'rqutPrdCn',
     'qualifications',
     'plcyTpNm',
     )

@admin.register(models.Subscribe)
class Subscribe(admin.ModelAdmin):
     list_display= (
     'id',
     'colored',
    'support_id',
     )


@admin.register(models.Category)
class Category(admin.ModelAdmin):
     list_display= (
     'id',
     'colored',
     'category',
    'organizer_id',
    'support_id'
     )



@admin.register(models.Channel)
class Channel(admin.ModelAdmin):
     list_display= (
     'id',
    'channel_name',
    'support_id'
     )



@admin.register(models.SupportBookMark)
class SupportBookMark(admin.ModelAdmin):
     list_display= (
     'uuid',
    'support_id',
     'member_id',
     'folder'
     )




@admin.register(models.SupportNotification)
class SupportNotification(admin.ModelAdmin):
     list_display=(
     'pk',
     'name',
     'member_device_info',
     'enabled',
     'crontab',
     'interval',
    # 'organizer_id',
     'support_id',
     'noti_on_time',
     'interval_time'
    
     )

@admin.register(models.SupportScheduledNotification)
class SupportScheduledNotification(admin.ModelAdmin):
     list_display=(
     'member_device_info',
     'user_device_info',
     'sched_noti',
     'noti_on_time',
     'noti_on_or_off'
    
     )
