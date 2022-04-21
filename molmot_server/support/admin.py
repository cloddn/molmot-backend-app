from support import models
from django.contrib import admin

# Register your models here.
@admin.register(models.Organization)
class Organization(admin.ModelAdmin):
     list_display= (
    'name',
     'location',
     'link'
     )


@admin.register(models.Support)
class Support(admin.ModelAdmin):
     list_display= (
     'uuid',
    'title',
     'detail',
     'submit_link',
     'organizer',
     'start_date',
     'end_date',
     'qualifications',
     'located_in',
     'age',
     'gender',
     'number_of_households',
     'income_ratio'
     )

@admin.register(models.Subscribe)
class Subscribe(admin.ModelAdmin):
     list_display= (
    'organizer_id',
     'member_id'
     )

@admin.register(models.Channel)
class Channel(admin.ModelAdmin):
     list_display= (
    'organizer_id',
     'member_id'
     )