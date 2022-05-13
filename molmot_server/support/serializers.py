from parser import ParserError
from this import d
from django.forms import DateInput, ValidationError
from rest_framework import serializers
from dateutil.parser import parse
from support.models import Channel, RecordingList, Support,Subscribe,SupportNotification,SupportScheduledNotification,SupportBookMark,Organization
from user.models import Member,MemberFCMDevice
import datetime
from django_celery_beat.models import CrontabSchedule, PeriodicTask,IntervalSchedule
import json
from django.utils import timezone

class SmartOpenapiSupportSerializer(serializers.ModelSerializer):
    cnsgNmor=serializers.CharField(max_length=255) #organizer
    polyBizSjnm=serializers.CharField(max_length=255) #title
    polyItcnCn=serializers.CharField(max_length=255) #detail
    sporCn=serializers.CharField(max_length=None)#detail
    ageInfo=serializers.CharField(max_length=255) #qualifications
    empmSttsCn=serializers.CharField(max_length=255)#qualifications
    accrRqisCn=serializers.CharField(max_length=255)#qualifications
    majrRqisCn=serializers.CharField(max_length=255)#qualifications
    splzRlmRqisCn=serializers.CharField(max_length=255)#qualifications
    rqutUrla=serializers.CharField(max_length=255) #submit_link
    member_id=serializers.CharField(max_length=255) 
    polyBizSecd=serializers.CharField(max_length=255) 

    class Meta:
        model = Support
        fields = ('title','detail','submit_link','organizer','bizId','rqutPrdCn','located_in','cnsgNmor',
        'polyBizSjnm','polyItcnCn','plcyTpNm','sporCn','ageInfo','polyBizSecd',
        'empmSttsCn','accrRqisCn','majrRqisCn',
        'splzRlmRqisCn','rqutUrla','member_id')

    def validate(self, data):
        print(data)
        data['organizer']=data.get('cnsgNmor','').replace('\n',"%^^%")
        data['detail']=("정책 소개: "+data.get('polyItcnCn','')+"%^^%지원 내용: "+data.get('sporCn','')).replace('\n',"%^^%")
        data['submit_link']=data.get('rqutUrla','')
        data['qualifications']=("연령: "+data.get('ageInfo','')+"%^^%취업 상태: "+data.get('empmSttsCn','')+" 학력: "+data.get('accrRqisCn','')+" 전공: "+data.get('majrRqisCn','')+" 특화 분야: "+data.get('splzRlmRqisCn','')).replace('\n',"%^^%")  
        data['title']=data.get('polyBizSjnm','').replace('\n',"%^^%")
        member_id=data.get('member_id',None)
        sub_data,new=Support.objects.get_or_create(organizer=data['organizer'],detail=data['detail'],
            submit_link=data['submit_link'],
            qualifications=data['qualifications'],
            title=data['title'],bizId=data['bizId'],
            rqutPrdCn=data['rqutPrdCn'],
            plcyTpNm=data['plcyTpNm'],located_in=data['polyBizSecd'])
        #SupportBookMark.objects.get_or_create(support_id=sub_data,member_id=Member.objects.get(pk=member_id))
        #Channel.objects.get_or_create(channel_name="For. 경기도인 대학생",support_id=sub_data)
            #date_list = data['rqutPrdCn'].split('~')
            #start_time = date_list[0]
            #end_time = date_list[1]
            #start_time = start_time.replace(".","-").replace(" ","")
            #end_time = end_time.replace(".","-").replace(" ","")
            #start_time=parse(start_time)
            #end_time=parse(end_time)
            #KST = datetime.timezone(datetime.timedelta(hours=9))
            #start_time=datetime.datetime(timezone.now().year,start_time.month,start_time.day,9,00,tzinfo=KST)
            #end_time=datetime.datetime(timezone.now().year,end_time.month,end_time.day,18,00,tzinfo=KST)
            #rqutPrdCn=start_time.strftime("%Y-%m-%d")+" ~ "+end_time.strftime("%Y-%m-%d")
    
        return data

    
    def create(self, data):
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
    subs_field_name=serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = ('__all__')

    def validate(self, data):
        try:
            #data #오브젝트 형태로 전달
            sb_datas=Subscribe.objects.filter(subscribe_name=data['subscribe_name'])
            for sb_data in sb_datas:
                uuid=data['member_id'][0].uuid
                sb_data.member_id.add(uuid)
                data['member_id'][0].last_login=datetime.datetime.now()
                data['member_id'][0].save()
        except ValidationError as ex:
            print(ex)
            raise serializers.ValidationError({"success":False})

    def get_subs_field_name(self,data):
        return data.subscribe_name


class ChannelSerializer(serializers.ModelSerializer):
    support_name=serializers.SerializerMethodField()
    

    class Meta:
        model = Channel
        fields = ('organizer_id','member_id','channel_name','support_id','support_name')

    def validate(self, data):
        print(data)
        try:
            #오브젝트 형태로 전달
            #org_obj=Organization.objects.get(pk=data['organizer_id'])
            ch_datas=Channel.objects.filter(channel_name=data['organizer_id'])
            for ch_data in ch_datas:
                uuid=data['member_id'][0].uuid
                ch_data.member_id.add(uuid)
                data['member_id'][0].last_login=datetime.datetime.now()
                data['member_id'][0].save()
            return ch_data

        except ValidationError as ex:
            print(ex)
            raise serializers.ValidationError({"success":False})


    def get_support_name(self,data):
        return data.support_id.title



class SupportNotificationSerializer(serializers.ModelSerializer):
    interval=serializers.SerializerMethodField()
    d_day=serializers.SerializerMethodField()
    title=serializers.SerializerMethodField()
    on_time=serializers.SerializerMethodField()
    
    
    class Meta:
        model = SupportNotification
        fields = ('id','interval','name','title','task','enabled','d_day','on_time')

    def get_interval(self,data):
        return str(data.interval_time)

    def get_d_day(self,data):
        try:
            d_day=str((data.support_id.end_date.date()-datetime.date.today()).days)
            return d_day
        except:
            return ""
    def get_on_time(self,data):
        try:
            on_time=str(data.crontab.hour)+":"+str(data.crontab.minute)
            return on_time
        except:
            return ""

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
            schedule, is_created =CrontabSchedule.objects.get_or_create(
            minute=00,
            hour=17,
            day_of_month=datetime.datetime.today().day,
            month_of_year=datetime.datetime.today().month,
            timezone="Asia/Seoul"
            )
            KST = datetime.timezone(datetime.timedelta(hours=9))
            support_id=Support.objects.get(uuid=data['support_id'].uuid)
            support_id.interval_time=int(data['interval_data'])
            member_device_info=MemberFCMDevice.objects.get(user=data['member_id'])
            support_noti_id=SupportNotification.objects.get_or_create(
                support_id=support_id,
                member_device_info=member_device_info,
                noti_on_time=datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,17,00),
                crontab=schedule,
                start_time=timezone.now(),
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
        try:
            support_id=Support.objects.get(uuid=data['support_id'].uuid)
            d_day=str((support_id.end_date.date()-datetime.date.today()).days)
            return d_day
        except:
            return ""

    def get_title(self,data):
        support_id=Support.objects.get(uuid=data['support_id'].uuid)
        return support_id.title
    
    
    def get_end_date(self,data):
        support_id=Support.objects.get(uuid=data['support_id'].uuid)
        return support_id.end_date


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
