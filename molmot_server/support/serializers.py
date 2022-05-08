from django.forms import DateInput, ValidationError
from rest_framework import serializers

from support.models import Channel, RecordingList, Support,Subscribe,SupportNotification,SupportScheduledNotification,SupportBookMark,Organization
from user.models import Member,MemberFCMDevice
import datetime
from django_celery_beat.models import CrontabSchedule, PeriodicTask,IntervalSchedule
import json

class SupportSerializer(serializers.ModelSerializer):
    hits=serializers.SerializerMethodField()

    class Meta:
        model = Support
        fields = ('__all__')
    
    def get_hits(self,obj):
        obj.click
        return obj.hits

class HomeSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Support
        fields = ('title',)
    

class RecordingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingList
        fields = ('__all__')

    def validate(self, data):
        try:
            #data #오브젝트 형태로 전달
            sub_data,new=RecordingList.objects.get_or_create(support_id=data['support_id'],member_id=data['member_id'])
            return sub_data
        except ValidationError as ex:
            print(ex)
            raise serializers.ValidationError({"success":False})


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('__all__')

    def validate(self, data):
        try:
            #data #오브젝트 형태로 전달
            sub_data,new=Subscribe.objects.get_or_create(organizer_id=data['organizer_id'],member_id=data['member_id'])
            return sub_data
        except ValidationError as ex:
            print(ex)
            raise serializers.ValidationError({"success":False})


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('__all__')

    def validate(self, data):
        try:
            print(data)#오브젝트 형태로 전달
            ch_data,new=Channel.objects.get_or_create(organizer_id=data['organizer_id'],member_id=data['member_id'])
            data['member_id'].last_login=datetime.datetime.now()
            data['member_id'].save()
            return ch_data

        except ValidationError as ex:
            print(ex)
            raise serializers.ValidationError({"success":False})


class SupportNotificationSerializer(serializers.ModelSerializer):
    interval=serializers.SerializerMethodField()
    d_day=serializers.SerializerMethodField()
    title=serializers.SerializerMethodField()
    
    
    class Meta:
        model = SupportNotification
        fields = ('interval','d_day','name','title','task','enabled','noti_on_time')

    def get_interval(self,data):
        text=str(data.interval.period)+str(data.interval.every)
        return text

    def get_d_day(self,data):
        d_day=str((data.support_id.end_date.date()-datetime.date.today()).days)
        return d_day

    def get_title(self,data):
        return str(data.support_id.title)

    def update(self, instance, validated_data):
        SupportNotification.objects.filter(pk=instance.pk)\
                            .update(**validated_data)
        return SupportNotification.objects.get(pk=instance.pk)

class HomeSupportNotificationSerializer(serializers.ModelSerializer):
    support_id=serializers.SerializerMethodField()
    
    class Meta:
        model = SupportNotification
        fields = ('support_id',)
    
    def get_support_id(self,data):
        return data.support_id.title


class SupportBookMarkSerializer(serializers.ModelSerializer):
    interval_data=serializers.CharField(max_length=30,default="7")
    d_day=serializers.SerializerMethodField()
    title=serializers.SerializerMethodField()
    end_date=serializers.SerializerMethodField()


    class Meta:
        model = SupportBookMark
        fields = ('uuid','support_id','member_id','d_day','title','end_date','interval_data')

    def validate(self, data):
        try:
            support_id=Support.objects.get(title=data['support_id'])
            interval=IntervalSchedule.objects.get_or_create(every=data['interval_data'],period="days")[0]
            member_device_info=MemberFCMDevice.objects.get(user=data['member_id'])
            support_noti_id=SupportNotification.objects.get_or_create(
                support_id=support_id,
                member_device_info=member_device_info,
                noti_on_time=support_id.start_date,
                interval=interval,
                start_time=datetime.datetime.now(),
                one_off=False,
                enabled=True,
                name=str(member_device_info.user)+"의 지원금"+str(support_id)+"알림",          
                task='support.tasks.support_notification_push',
                kwargs=json.dumps({'support_id':str(support_id.uuid),'member_id':str(data['member_id'])})
                )[0]
            print(support_noti_id)
            support_noti_id.save()
        except Support.DoesNotExist:
            pass
        except ValidationError as ex:
            print(ex)
            raise serializers.ValidationError({"success":False})
        return data

    def get_d_day(self,data):
        d_day=str((data.support_id.end_date.date()-datetime.date.today()).days)
        return d_day

    def get_title(self,data):
        return data.support_id.title
    
    def get_end_date(self,data):
        return data.support_id.end_date
'''
def create(self,validated_data):
        print("생성")
        group = Group.objects.create(**validated_data) 
        group.save()
        return group

    def update(self, instance, validated_data):
        group = Group.objects.get(pk=instance.uuid)
        Group.objects.filter(pk=instance.uuid)\
                           .update(**validated_data)
        return group
'''
