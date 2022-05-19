from ast import Or
from io import BytesIO
from parser import ParserError
from django.forms import DateInput, ValidationError
from rest_framework import serializers
from dateutil.parser import parse
from media.models import SmartResultQRPhoto
from support.helper import qrcode_selfie_num
from support.models import Category, Channel, RecordingList, Support,Subscribe,SupportNotification,SupportBookMark,Organization
from user.models import Member,MemberFCMDevice
import datetime
from django_celery_beat.models import CrontabSchedule, PeriodicTask,IntervalSchedule
import json
from django.utils import timezone
import qrcode
from django.core.files.base import File

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
        'splzRlmRqisCn','rqutUrla','member_id','job_info','detail_field')

    def validate(self, data):
        data['organizer']=data.get('cnsgNmor','').replace('\n',"%^^%")
        data['detail']=("정책 소개: "+data.get('polyItcnCn','')+"%^^%지원 내용: "+data.get('sporCn','')).replace('\n',"%^^%")
        data['submit_link']=data.get('rqutUrla','')
        data['qualifications']=("연령: "+data.get('ageInfo','')+"%^^%취업 상태: "+data.get('empmSttsCn','')+" 학력: "+data.get('accrRqisCn','')+" 전공: "+data.get('majrRqisCn','')+" 특화 분야: "+data.get('splzRlmRqisCn','')).replace('\n',"%^^%")  
        data['title']=data.get('polyBizSjnm','').replace('\n',"%^^%")
        member_id=data.get('member_id',None)
        located_in=data['polyBizSecd']
        submit_link=data['submit_link']
        bizId=data['bizId']
        Support.objects.filter(title='').delete()
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


class SmartOpenapiCreateSupportSerializer(serializers.ModelSerializer):
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
    qr_code_link=serializers.SerializerMethodField()

    class Meta:
        model = Support
        fields = ('title','detail','submit_link','organizer','bizId','rqutPrdCn','located_in','cnsgNmor',
        'polyBizSjnm','polyItcnCn','plcyTpNm','sporCn','ageInfo','polyBizSecd',
        'empmSttsCn','accrRqisCn','majrRqisCn',
        'splzRlmRqisCn','rqutUrla','member_id','job_info','qr_code_link','detail_field')

    def validate(self, data):
        print(data)
        data['organizer']=data.get('cnsgNmor','').replace('\n',"%^^%")
        data['detail']=("정책 소개: "+data.get('polyItcnCn','')+"%^^%지원 내용: "+data.get('sporCn','')).replace('\n',"%^^%")
        data['submit_link']=data.get('rqutUrla','')
        data['qualifications']=("연령: "+data.get('ageInfo','')+"%^^%취업 상태: "+data.get('empmSttsCn','')+" 학력: "+data.get('accrRqisCn','')+" 전공: "+data.get('majrRqisCn','')+" 특화 분야: "+data.get('splzRlmRqisCn','')).replace('\n',"%^^%")  
        data['title']=data.get('polyBizSjnm','').replace('\n',"%^^%")
        member_id=data.get('member_id',None)
        if (Support.objects.filter(bizId=data['bizId']).count()>2):
            Support.objects.filter(organizer=data['organizer'],detail=data['detail'],
            submit_link=data['submit_link'],
            qualifications=data['qualifications'],
            title=data['title'],bizId=data['bizId']).delete()
        sub_data,new=Support.objects.get_or_create(organizer=data['organizer'],detail=data['detail'],
            submit_link=data['submit_link'],
            qualifications=data['qualifications'],
            title=data['title'],bizId=data['bizId'],
            rqutPrdCn=data['rqutPrdCn'],
            plcyTpNm=data['plcyTpNm'],job_info=data['job_info'],detail_field=data['detail_field'],located_in=data['polyBizSecd'],plcyTpNm_detail="심리지원")
        obj=Member.objects.get(pk=member_id)
        obj.is_smart_recommed=True
        obj.save()
        SupportBookMark.objects.get_or_create(support_id=sub_data,member_id=obj,folder="smart")
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

    def get_qr_code_link(self,data):
        member_id=data.get('member_id',None)
        url = 'http://ec2-3-36-93-17.ap-northeast-2.compute.amazonaws.com/user/index/'+member_id+'/'
        qr_img = qrcode.make(url)
        qr_img.convert('RGB') # convert mode

        thumb_io = BytesIO() # create a BytesIO object

        qr_img.save(thumb_io, 'JPEG', quality=100) # save image to BytesIO object
        name=qrcode_selfie_num()+member_id+".jpg"
        qr_file = File(thumb_io, name=name)
        sm_obj,is_created=SmartResultQRPhoto.objects.get_or_create(member_id=Member.objects.get(pk=member_id),photo_file=qr_file)
    
        return sm_obj.photo_file.url

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
    polyBizSecd=serializers.CharField(max_length=255)
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
        'empmSttsCn','accrRqisCn','majrRqisCn','polyBizSecd',
        'splzRlmRqisCn','rqutUrla')

    
    def validate(self, data):
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
            plcyTpNm=data['plcyTpNm'],located_in=data['polyBizSecd'],plcyTpNm_detail="문화")
        Channel.objects.get_or_create(organizer_id=Organization.objects.get(pk="ed427564-715a-49ad-8b93-1410e6f4dbfd"),channel_name="서울 청년 혜택 모음",support_id=sub_data)
        return data


class SupportSerializer(serializers.ModelSerializer):
    hits=serializers.SerializerMethodField()

    class Meta:
        model = Support
        fields = ('__all__')
    
    def get_hits(self,obj):
        obj.click
        return obj.hits


class CategorywithSupportSerializer(serializers.ModelSerializer):
    detail_field=serializers.SerializerMethodField()
    job_info=serializers.SerializerMethodField()
    

    class Meta:
        model = Support
        fields = ('uuid','title','plcyTpNm','detail_field','job_info')

    def get_detail_field(self,data):
        return data.get_detail_field_display()
    
    def get_job_info(self,data):
        return data.get_job_info_display()
    
    

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



class CategorySerializer(serializers.ModelSerializer):
    support_id=CategorywithSupportSerializer()

    class Meta:
        model = Category
        fields = ('__all__')

class ChannelSerializer(serializers.ModelSerializer):
    support_name=serializers.SerializerMethodField()
    

    class Meta:
        model = Channel
        fields = ('organizer_id','member_id','channel_name','support_id','support_name')

    def validate(self, data):
        print(data)
        try:
            #오브젝트 형태로 전달
            if (data.get('organizer_id',None)!=None):
            #org_obj=Organization.objects.get(pk=data['organizer_id'])
                ch_datas=Channel.objects.filter(organizer_id=data['organizer_id'])
                for ch_data in ch_datas:
                    print(len(ch_datas))
                    uuid=data['member_id'][0]
                    ch_data.member_id.add(uuid)
                    ch_data.save()
                    #data['member_id'].last_login=datetime.datetime.now()
                    #data['member_id'].save()
                    return ch_data
            elif (data.get('organizer_id',None)==None):
                data=Channel.objects.filter(member_id__in=["2a8f72ed-1090-421a-903a-510aa1f809a3"])
                return data
            else:
                return data
        except KeyError or ValidationError as ex:
            #ch_datas=Channel.objects.filter(channel_name=data['organizer_id'])
            return data




class ChannelGetListSerializer(serializers.ModelSerializer):
    support_name=serializers.SerializerMethodField()
    detail_field=serializers.SerializerMethodField()
    plcyTpNm_detail=serializers.SerializerMethodField()
    plcyTpNm=serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ('channel_name','support_id','support_name','detail_field','plcyTpNm_detail','plcyTpNm')

   

    def get_support_name(self,data):
        return data.support_id.title
    def get_detail_field(self,data):
        return data.support_id.get_detail_field_display()

    def get_plcyTpNm_detail(self,data):
        return data.support_id.plcyTpNm_detail

    
    def get_plcyTpNm(self,data):
        return data.support_id.plcyTpNm

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
            if (len(str(data.crontab.minute))==1):
                on_time=str(data.crontab.hour)+":"+str(data.crontab.minute)+"0"
            elif (len(str(data.crontab.hour))==1):
                on_time="0"+str(data.crontab.hour)+":"+str(data.crontab.minute)
            elif (len(str(data.crontab.hour))==1 )and (len(str(data.crontab.minute))==1):
                on_time="0"+str(data.crontab.hour)+":"+str(data.crontab.minute)+"0"
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
        fields = ('uuid','support_id','d_day','member_id','title','end_date','interval_data','folder')

    def validate(self, data):
        try:
            schedule,is_created =CrontabSchedule.objects.get_or_create(
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

            d_day=str((data.support_id.end_date.date()-datetime.date.today()).days)
            return d_day
        except:
            return ""

    def get_title(self,data):
        try:
            return data.support_id.title
        except:
            return data.support_id
    
    
    def get_end_date(self,data):
        try:
            return data.support_id.end_date
        except:
            return data.support_id


class SupportBookMarkCreateSerializer(serializers.ModelSerializer):
    interval_data=serializers.CharField(max_length=30,default="7")


    class Meta:
        model = SupportBookMark
        fields = ('uuid','support_id','member_id','interval_data','folder')

    def validate(self, data):
        try:
            schedule,is_created =CrontabSchedule.objects.get_or_create(
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
            try:
                SupportBookMark.objects.get_or_create(support_id=support_id,member_id=data['member_id'],folder=data['folder'])   
            except:
                SupportBookMark.objects.get_or_create(support_id=support_id,member_id=data['member_id'],folder="general")   
            print(support_noti_id)
            support_noti_id.save()
        except Support.DoesNotExist:
            pass
        except ValidationError as ex:
            print(ex)
            raise serializers.ValidationError({"success":False})
        return data

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


class SupportInfoViewSerializers(serializers.ModelSerializer):
    polyBizSjnm=serializers.CharField(max_length=255) #title
    polyItcnCn=serializers.CharField(max_length=255) #detail
    sporCn=serializers.CharField(max_length=None)#detail
    ageInfo=serializers.CharField(max_length=255) #qualifications
    empmSttsCn=serializers.CharField(max_length=255)#qualifications
    accrRqisCn=serializers.CharField(max_length=255)#qualifications
    majrRqisCn=serializers.CharField(max_length=255)#qualifications
    splzRlmRqisCn=serializers.CharField(max_length=255)#qualifications
    rqutUrla=serializers.CharField(max_length=255) #submit_link
    polyBizSecd=serializers.CharField(max_length=255) 
    

    class Meta:
        model = Support
        fields = ('title','detail','submit_link','organizer','bizId','rqutPrdCn','located_in',
        'polyBizSjnm','polyItcnCn','plcyTpNm','sporCn','ageInfo','polyBizSecd',
        'empmSttsCn','accrRqisCn','majrRqisCn','qualifications',
        'splzRlmRqisCn','rqutUrla','job_info','detail_field')

    def validate(self, data):
        data['detail']=data.get('polyItcnCn','')
        data['submit_link']=data.get('rqutUrla','')
        data['qualifications']=("연령: "+data.get('ageInfo','')+"%^^%취업 상태: "+data.get('empmSttsCn','')+" 학력: "+data.get('accrRqisCn','')+" 전공: "+data.get('majrRqisCn','')+" 특화 분야: "+data.get('splzRlmRqisCn','')).replace('\n',"%^^%")  
        data['title']=data.get('polyBizSjnm','').replace('\n',"%^^%")
        member_id=data.get('member_id',None)
        located_in=data['polyBizSecd']
        submit_link=data['submit_link']
        bizId=data['bizId']
        Support.objects.filter(title='').delete()
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
