from this import d
from django.forms import DateInput, ValidationError
from rest_framework import serializers

from support.models import Channel, RecordingList, Support,Subscribe,SupportNotification,SupportScheduledNotification,SupportBookMark,Organization
from user.models import Member,MemberFCMDevice
import datetime
from django_celery_beat.models import CrontabSchedule, PeriodicTask,IntervalSchedule
import json

class SmartOpenapiSupportSerializer(serializers.ModelSerializer):
    polyBizTy=serializers.CharField(max_length=255) #organizer
    polyBizSjnm=serializers.CharField(max_length=255) #title
    polyItcnCn=serializers.CharField(max_length=255) #detail
    sporCn=serializers.CharField(max_length=255)#detail
    ageInfo=serializers.CharField(max_length=255) #qualifications
    empmSttsCn=serializers.CharField(max_length=255)#qualifications
    accrRqisCn=serializers.CharField(max_length=255)#qualifications
    majrRqisCn=serializers.CharField(max_length=255)#qualifications
    splzRlmRqisCn=serializers.CharField(max_length=255)#qualifications
    rqutUrla=serializers.CharField(max_length=255) #submit_link
    member_id=serializers.CharField(max_length=255) 

    class Meta:
        model = Support
        fields = ('title','detail','submit_link','organizer','bizId','rqutPrdCn','located_in','polyBizTy',
        'polyBizSjnm','polyItcnCn','plcyTpNm','sporCn','ageInfo',
        'empmSttsCn','accrRqisCn','majrRqisCn',
        'splzRlmRqisCn','rqutUrla','member_id')

    def validate(self, data):
        data['organizer']=data.get('polyBizTy','').replace('\n',"%^^%")
        data['detail']=("정책 소개: "+data.get('polyItcnCn','')+" 지원 내용: "+data.get('sporCn','')).replace('\n',"%^^%")
        data['submit_link']=data.get('rqutUrla','')
        data['qualifications']=("연령: "+data.get('ageInfo','')+" 취업 상태: "+data.get('empmSttsCn','')+" 학력: "+data.get('accrRqisCn','')+" 전공: "+data.get('majrRqisCn','')+" 특화 분야: "+data.get('splzRlmRqisCn','')).replace('\n',"%^^%")  
        data['title']=data.get('polyBizSjnm','').replace('\n',"%^^%")
        member_id=data.get('member_id',None)
        sub_data,new=Support.objects.get_or_create(organizer=data['organizer'],detail=data['detail'],
        submit_link=data['submit_link'],qualifications=data['qualifications'],title=data['title'],bizId=data['bizId'],rqutPrdCn=data['rqutPrdCn'],plcyTpNm=data['plcyTpNm'])
        SupportBookMark.objects.get_or_create(support_id=sub_data,member_id=Member.objects.get(pk=member_id))
        print(data)
        return data
    
    def create(self, data):
        print(data)
        sub_data,new=Support.objects.get_or_create(**data)
        member_id=data.pop('member_id',None)
        #Support.objects.filter(bizId=data['bizId']).delete()

    ''''
    def create(self, data):
        print(data)
        organizer=data.pop('polyBizTy','').replace('\n',"%^^%")
        title=data.pop('polyBizSjnm','').replace('\n',"%^^%")
        detail=("정책 소개: "+data.pop('polyItcnCn','')+" 지원 내용: "+data.pop('sporCn','')).replace('\n',"%^^%")
        qualifications=("연령: "+data.pop('ageInfo','')+" 취업 상태: "+data.pop('empmSttsCn','')+" 학력: "+data.pop('accrRqisCn','')+" 전공: "+data.pop('majrRqisCn','')+" 특화 분야: "+data.pop('splzRlmRqisCn','')).replace('\n',"%^^%")
        submit_link=data.pop('rqutUrla','')
        member_id=data.pop('member_id',None).replace('\n',"%^^%")
        sub_data,new=Support.objects.get_or_create(organizer=organizer,title=title,detail=detail,qualifications=qualifications,
        
        submit_link=submit_link,**data)
        SupportBookMark.objects.get_or_create(support_id=sub_data,member_id=Member.objects.get(pk=member_id))
        #Support.objects.filter(bizId=data['bizId']).delete()
        print("123"+Support.objects.get(pk='f47fad85-6059-4e53-8ec9-fe97c13b3c57').title)
'''
class OpenapiSupportSerializer(serializers.ModelSerializer):
    polyBizTy=serializers.CharField(max_length=255) #organizer
    polyBizSjnm=serializers.CharField(max_length=255) #title
    polyItcnCn=serializers.CharField(max_length=255) #detail
    sporCn=serializers.CharField(max_length=255)#detail
    ageInfo=serializers.CharField(max_length=255) #qualifications
    empmSttsCn=serializers.CharField(max_length=255)#qualifications
    accrRqisCn=serializers.CharField(max_length=255)#qualifications
    majrRqisCn=serializers.CharField(max_length=255)#qualifications
    splzRlmRqisCn=serializers.CharField(max_length=255)#qualifications
    rqutUrla=serializers.CharField(max_length=255) #submit_link

    class Meta:
        model = Support
        fields = ('title','detail','submit_link','organizer','bizId','rqutPrdCn','located_in','polyBizTy',
        'polyBizSjnm','polyItcnCn','plcyTpNm','sporCn','ageInfo',
        'empmSttsCn','accrRqisCn','majrRqisCn',
        'splzRlmRqisCn','rqutUrla','member_id')

    
    def validate(self, data):
        data['organizer']=data.get('polyBizTy','').replace('\n',"%^^%")
        data['detail']=("정책 소개: "+data.get('polyItcnCn','')+" 지원 내용: "+data.get('sporCn','')).replace('\n',"%^^%")
        data['submit_link']=data.get('rqutUrla','')
        data['qualifications']=("연령: "+data.get('ageInfo','')+" 취업 상태: "+data.get('empmSttsCn','')+" 학력: "+data.get('accrRqisCn','')+" 전공: "+data.get('majrRqisCn','')+" 특화 분야: "+data.get('splzRlmRqisCn','')).replace('\n',"%^^%")  
        data['title']=data.get('polyBizSjnm','').replace('\n',"%^^%")
        return data

    def create(self, data):
        sub_data,new=Support.objects.get_or_create(**data)
      
        #Support.objects.filter(bizId=data['bizId']).delete()



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
        fields = ('id','interval','name','title','task','enabled','d_day')

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
        fields = ('uuid','support_id','d_day','member_id','title','end_date','interval_data')

    def validate(self, data):
        try:
            KST = datetime.timezone(datetime.timedelta(hours=9))
            support_id=Support.objects.get(title=data['support_id'])
            interval=IntervalSchedule.objects.get_or_create(every=data['interval_data'],period="days")[0]
            member_device_info=MemberFCMDevice.objects.get(user=data['member_id'])
            interval=IntervalSchedule.objects.get_or_create(every="7",period="days")[0]       
            support_noti_id=SupportNotification.objects.get_or_create(
                support_id=support_id,
                member_device_info=member_device_info,
                noti_on_time=datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,17,00),
                interval=interval,
                last_run_at=datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,17,00,tzinfo=KST)-datetime.timedelta(days=interval.every),
                start_time=datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,17,00,tzinfo=KST),
                one_off=False,
                enabled=True,
                name=str(member_device_info.user)+"의 지원금"+support_id.title+"알림",          
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
