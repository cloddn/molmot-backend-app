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


@admin.register(models.Supports)
class Supports(admin.ModelAdmin):
     list_display= (
    'title',
     'detail',
     'submit_link',
     'organizer',
     'start_date',
     'end_date',
     'qualifications'
     )