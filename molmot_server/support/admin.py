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
     'located_in',
     'bizId',
    'title',
     'detail',
     'submit_link',
     'organizer',
     'start_date',
     'end_date',
     'rqutPrdCn',
     'qualifications',
     'plcyTpNm',
     'interval_time'
     )

@admin.register(models.Subscribe)
class Subscribe(admin.ModelAdmin):
     list_display= (
     'id',
     'colored',
    'organizer_id',
     'member_id'
     )


@admin.register(models.Channel)
class Channel(admin.ModelAdmin):
     list_display= (
     'id',
     'category',
    'channel_name',
    'organizer_id',
     'member_id'
     )



@admin.register(models.SupportBookMark)
class SupportBookMark(admin.ModelAdmin):
     list_display= (
     'uuid',
    'support_id',
     'member_id'
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
     'noti_on_time'
    
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
