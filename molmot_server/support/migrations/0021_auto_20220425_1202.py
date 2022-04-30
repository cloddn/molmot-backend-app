# Generated by Django 3.2.12 on 2022-04-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0020_auto_20220425_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportschedulednotification',
            name='noti_on_or_off',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='supportschedulednotification',
            name='noti_on_time',
            field=models.DateTimeField(null=True, verbose_name='푸시알림 전송할 시간'),
        ),
    ]