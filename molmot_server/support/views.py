
import datetime
from pymysql import NULL
from webdriver_manager.chrome import ChromeDriverManager
import random

from unicodedata import category
from wsgiref.simple_server import demo_app
from django.http import JsonResponse
from requests import api, delete, request
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics # generics class-based view 사용할 계획
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action,permission_classes, authentication_classes
from django.forms.models import model_to_dict
# JWT 사용을 위해 필요
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from support.open_api import get_youth_center
from support.seoul_youth import get_seoul_youth_list

from user.utils import login_check
from django.core import serializers as core_serializers

from .serializers import *
from .models import *
from rest_framework.views import APIView
from django.db.models import Q
import json
from django.utils.decorators import method_decorator
from rest_framework import viewsets


from rest_framework import status, viewsets
from rest_framework.response import Response
from dateutil.parser import parse
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@authentication_classes([]) 
@permission_classes([]) 
class SupportFilterInfoView(APIView):

    def get(self,request):
        located_in               = request.GET.getlist('located_in', None)
        gender              = request.GET.getlist('gender', None)
        number_of_households= request.GET.getlist('number_of_households', None)
        income_ratio=request.GET.getlist('income_ratio', None)
        #start_date_range  = request.GET.get('StartDate',datetime.datetime(2018, 1, 31, 0, 0))
        #end_date_range  = request.GET.get('EndDate', datetime.datetime(2023, 1, 31, 0, 0))

        q=Q()
        if located_in:
            q &= Q(located_in__in= located_in)
        if gender:
            q &= Q(gender = gender)
        if number_of_households:
            q &= Q(number_of_households__in = int(number_of_households))
        if income_ratio:
            q &= Q(income_ratio__in=income_ratio)
            
        #q &= Q(price__range = (start_date_range,end_date_range))
                    
        supports = Support.objects.filter(q).order_by('-start_date')[:5]

        filter_options = {
            'located_in': 'located_in__in',
            'number_of_households': 'number_of_households__in',
            'income_ratio':'income_ratio__in',
            'gender':'gender',
            #'start_date_lower_range_range': 'start_date__gte',
            #'start_date_upper_range_range': 'start_date__lte',
            #'end_date_lower_range_range': 'end_date__gte',
            #'end_date_upper_range_range': 'end_date__lte',
        }

        filter_set = {
            filter_options.get(key) : value for (key, value) in dict(request.GET).items() if filter_options.get(key)
        }
        
        supports = Support.objects.filter(**filter_set).distinct()
        data = list(supports.values())
        return Response(data)  
    
    
    def post(self,request):
        located_in               = request.GET.getlist('located_in', None)
        gender              = request.GET.getlist('gender', None)
        number_of_households= request.GET.getlist('number_of_households', None)
        income_ratio=request.GET.getlist('income_ratio', None)
        #start_date_range  = request.GET.get('StartDate',datetime.datetime(2018, 1, 31, 0, 0))
        #end_date_range  = request.GET.get('EndDate', datetime.datetime(2023, 1, 31, 0, 0))

        print(request.GET)
        print(request.data.get('member_id',None))
        q=Q()
        if located_in:
            q &= Q(located_in__in= located_in)
        if gender:
            q &= Q(gender = gender)
        if number_of_households:
            q &= Q(number_of_households__in = int(number_of_households))
        if income_ratio:
            q &= Q(income_ratio__in=income_ratio)
            
        #q &= Q(price__range = (start_date_range,end_date_range))
                    
        supports = Support.objects.filter(q).order_by('-start_date')[:5]

    


        filter_options = {
            'located_in': 'located_in__in',
            'number_of_households': 'number_of_households__in',
            'income_ratio':'income_ratio__in',
            'gender':'gender',
            #'start_date_lower_range_range': 'start_date__gte',
            #'start_date_upper_range_range': 'start_date__lte',
            #'end_date_lower_range_range': 'end_date__gte',
            #'end_date_upper_range_range': 'end_date__lte',
        }

        filter_set = {
            filter_options.get(key) : value for (key, value) in dict(request.GET).items() if filter_options.get(key)
        }
        
        supports = Support.objects.filter(**filter_set).distinct()
        #즐겨찾기 연결 -> 몇개 나오게 할 건지, 생각!!!!
        #SupportBookMark.objects.create
        data = list(supports.values())
        for i in data:
            print(i)
            SupportBookMark.objects.get_or_create(support_id=Support.objects.get(uuid=i['uuid']),member_id=Member.objects.get(pk=request.data.get('member_id',None)))
        return Response(data)  

@authentication_classes([]) 
@permission_classes([]) 
class SupportInfoView(APIView):
    def get(self,request,*args, **kwargs):
        try:
            sup_obj=Support.objects.get(pk=kwargs['support_id'])
            query={
            "openApiVlak":"167693bf2984bec5368623af",
            "display":15,
            "pageIndex":1,
            "srchPolicyId":sup_obj.bizId
            }
            dict2_type=get_youth_center(query)
            support_dict=dict2_type['empsInfo']['emp']
            support_dict['job_info']=sup_obj.job_info
            support_dict['plcyTpNm_detail']=sup_obj.plcyTpNm_detail
            support_dict['detail_field']=sup_obj.detail_field
            serializers=SupportInfoViewSerializers(data=support_dict)
            if serializers.is_valid():
                return_data={}
                return_data['rqutPrdCn']=serializers.data.get('rqutPrdCn',"-")
                return_data['qualifications']=serializers.data.get('qualifications',"-")
                return_data['sporCn']=serializers.data.get('sporCn',"-")
                return_data['rqutUrla']=serializers.data.get('rqutUrla',"-")
                if return_data['rqutUrla']=="null" or return_data['rqutUrla']==NULL:
                    return_data['rqutUrla']="-"
                
                return_data['title']=serializers.data.get('title',"-")
                return_data['detail']=serializers.data.get('detail',"-")
                return_data['submit_link']=return_data['rqutUrla']
                return_data['job_info']=serializers.data.get('job_info',"-")
                return_data['organizer']=serializers.data.get('organizer',"-")
                if return_data['organizer']=="null" or return_data['organizer']==NULL:
                    return_data['organizer']="-"

                return_data['polyItcnCn']=serializers.data.get('polyItcnCn',"-")
                return_data['plcyTpNm']=serializers.data.get('plcyTpNm',"-")

                return Response({"success":return_data})
            else: return Response({"success":False})
        except Exception as e:
            print(e)
            return Response({"success":False})
        

@authentication_classes([]) 
@permission_classes([])
class SubscribeInfoView(generics.ListAPIView):
    serializer_class=SubscribeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        member_id=self.kwargs['member_id']
        return Subscribe.objects.filter(member_id__id=member_id)





@authentication_classes([])
@permission_classes([]) 
class SupportNotificationViewSet(viewsets.ModelViewSet):
    queryset = SupportNotification.objects.all()
    serializer_class = SupportNotificationSerializer



    def get_queryset(self):
        if self.kwargs.get('pk',None)!=None:
            pk=self.kwargs.get('pk',None)
            print(super().get_queryset().filter(pk=pk))
            return super().get_queryset().filter(pk=pk)
        else:
            return super().get_queryset()

    def create(self,request,*args,**kwargs):
        try:
            #신청 날짜 지나면 마감 하루 일자 하루전 , 안지났으면 시작 일자 7일 동안 울리게 
            #기기 토큰 1개만 가지고 있을 수 있도록...?
            time_data=parse(request.data.get('start_run'))
            interval=request.data.get('interval','7')
            support_id=Support.objects.get(uuid=request.data.get('support_id',None))
            #member_id 
            schedule =CrontabSchedule.objects.create(
            minute=time_data.minute,
            hour=time_data.hour,
            day_of_month=datetime.datetime.today().day,
            month_of_year=datetime.datetime.today().month,
            timezone="Asia/Seoul"
            )
            KST = datetime.timezone(datetime.timedelta(hours=9))
            member_device_info=MemberFCMDevice.objects.get(user=request.data.get('member_id','None'))
            #알림서비스 새로 만들기 
            SupportNotification.objects.get_or_create(
                member_device_info=member_device_info,
                support_id=support_id,
                noti_on_time=datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,17,00,tzinfo=KST),
                crontab=schedule,
                interval_time=interval,
                start_time=timezone.now(),
                name=str(member_device_info.user)+"의 지원금"+support_id.title+"알림",          
                task='support.tasks.support_notification_push',
                kwargs=json.dumps({'support_id':str(support_id.uuid),'member_id':request.data.get('member_id','None')}))
            return Response({"success":True}, status=status.HTTP_201_CREATED)
        except Support.DoesNotExist or MemberFCMDevice.DoesNotExist:
            pass
        except:
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)
        
   
    
    def update(self,request, *args, **kwargs):
        print(request.data)
        print(kwargs['pk'])
        
        supno_obj=SupportNotification.objects.get(pk=kwargs['pk'])
        if (request.data.get('interval',None)!=None):
            supno_obj.interval_time=int(request.data.get('interval',None))
            supno_obj.enabled=True
            supno_obj.save()
        if (request.data.get('enabled',None)!=None):
            bool_data=True if request.data.get('enabled',None)==True else False
            print(bool_data)
            supno_obj.enabled=bool_data
            supno_obj.save()
        if (request.data.get('start_run',None)!=None):
            time_data=parse(request.data.get('start_run'))
            supno_obj.crontab.minute=time_data.minute
            supno_obj.crontab.hour=time_data.hour
            supno_obj.crontab.save()
            #supno_obj.crontab.day_of_month=time_data.day_of_month
            #supno_obj.crontab.month_of_year=time_data.month_of_year
            print(datetime.datetime.today())
            print(supno_obj.crontab)
            supno_obj.save()
        return Response({"success":True}, status=status.HTTP_201_CREATED)
    

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return Response({"success":True}, status=status.HTTP_200_OK)
        except:
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([])
@permission_classes([]) 
class SubscribeViewSet(viewsets.ModelViewSet):

    
    #I took the liberty to change the model to queryset
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer



    def get_queryset(self):
        if self.kwargs.get('pk',None)!=None:
            member_id=self.kwargs.get('pk',None)
            return super().get_queryset().filter(member_id__in=[member_id])
        else:
            return super().get_queryset()

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
            if serializer.is_valid():
                headers = self.get_success_headers(serializer.data)
                return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                print(serializer.errors)
                return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([])
@permission_classes([]) 
class ChannelViewSet(viewsets.ModelViewSet):

    
    #I took the liberty to change the model to queryset
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer



    def get_queryset(self):
        if self.kwargs.get('pk',None)!=None:
            pk=self.kwargs.get('pk',None)
            return super().get_queryset().filter(pk=pk)
        else:
            return super().get_queryset()

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        if serializer.is_valid():
            headers = self.get_success_headers(serializer.data)
            return Response({"success":True}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(serializer.errors)
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([])
@permission_classes([]) 
class ChannelsView(generics.ListAPIView,generics.ListCreateAPIView):
    serializer_class=ChannelSerializer

    def get_queryset(self):
        if self.kwargs.get('member_id',None)!=None:
            member_id=self.kwargs.get('member_id',None)
            return Channel.objects.filter(member_id__in=[member_id])
        else:
            return Channel.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        for i in request.data:
            i['member_id']=[i['member_id']]
        #request.data['member_id']=list(request.data['member_id'])
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        if serializer.is_valid():
            headers = self.get_success_headers(serializer.data)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(serializer.errors)
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)
        
@authentication_classes([])
@permission_classes([]) 
class ChannelsNametoListView(generics.ListAPIView):
    serializer_class=ChannelGetListSerializer

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self.request.query_params.get('channel_name',None)!=None:
            channel_name=self.request.query_params.get('channel_name',None)
            return Channel.objects.filter(channel_name=channel_name)
        else:
            return Channel.objects.all()

    

       

@authentication_classes([])
@permission_classes([]) 
class GetCategoryListView(generics.ListAPIView,generics.ListCreateAPIView):
    serializer_class=CategorySerializer

    def get_queryset(self):
        if self.kwargs.get('colored',None)!=None:
            colored=self.kwargs.get('colored',None)
            return Category.objects.filter(colored=colored)
        else:
            return Category.objects.all()

    '''def create(self, request, *args, **kwargs):
        print(request.data)
        for i in request.data:
            i['member_id']=[i['member_id']]
        #request.data['member_id']=list(request.data['member_id'])
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        if serializer.is_valid():
            headers = self.get_success_headers(serializer.data)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(serializer.errors)
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)
    '''  
from django.db.models import Count


@authentication_classes([])
@permission_classes([]) 
class SupportBookMarkViewSet(viewsets.ModelViewSet):
    
    #I took the liberty to change the model to queryset
    queryset = SupportBookMark.objects.all()
    serializer_class = SupportBookMarkSerializer

    @action(methods=['POST'], detail=False)
    def bookmark_list_create(self,request, *args, **kwargs):
            serializer = SupportBookMarkCreateSerializer(data=request.data, many=isinstance(request.data,list))
            if serializer.is_valid():
                headers = SupportBookMarkCreateSerializer(serializer.data)
                return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def bookmark_list(self,request, *args, **kwargs):
        print(request.GET['member_id'])
        try:
            if request.GET['folder']!=None:
                member_id=request.GET['member_id']
                return Response(SupportBookMark.objects.filter(member_id=member_id,folder=request.GET['folder']).values())
        except KeyError:
            return Response(SupportBookMark.objects.filter(member_id=request.GET['member_id']).values())
        except:
            return Response(SupportBookMark.objects.all().values())

    def get_queryset(self,*args, **kwargs):
        if self.kwargs.get('member_id',None)!=None:
            member_id=self.kwargs.get('member_id',None)
            return super().get_queryset().filter(member_id=member_id,folder=self.kwargs.get('folder','general'))
        else:
            return super().get_queryset()

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
            if serializer.is_valid():
                headers = self.get_success_headers(serializer.data)
                return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                print(serializer.errors)
                return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return Response({"success":True}, status=status.HTTP_200_OK)
        except:
            return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([])
@permission_classes([]) 
class RecordingListViewSet(viewsets.ModelViewSet):

    
    #I took the liberty to change the model to queryset
    queryset = RecordingList.objects.all()
    serializer_class = RecordingListSerializer


    def get_queryset(self):
        if self.kwargs.get('member_id',None)!=None:
            member_id=self.kwargs.get('member_id',None)
            return super().get_queryset().filter(member_id=member_id)
        else:
            return super().get_queryset()

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
            if serializer.is_valid():
                headers = self.get_success_headers(serializer.data)
                return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([])
@permission_classes([]) 
class AllAlarmsONOFFView(APIView):
    def get(self,request,member_id,on_off):
        try:
            if (on_off=="OFF"):
                SupportNotification.objects.filter(member_device_info=MemberFCMDevice.objects.get(user=Member.objects.get(pk=member_id))).update(enabled=False,noti_on_or_off=False)
            elif (on_off=="ON"):
                SupportNotification.objects.filter(member_device_info=MemberFCMDevice.objects.get(user=Member.objects.get(pk=member_id))).update(enabled=True,noti_on_or_off=True)
            else:
                return Response({"success":False},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success":True},status=status.HTTP_200_OK)
        except:
            return Response({"success":False},status=status.HTTP_400_BAD_REQUEST)
       
#첫 로그인시 구독 분야 설정

# Reading the CSV to the model DB
'''
def extract_db(csvfile):
    with open('df.csv') as csvfile:         
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = Upload(Student_Name=row['Student Name'], Total_Marks=row['Total Marks'], Marks_Scored=row['Marks Scored'],
                                        Status=row['Status'], PhoneNumber=row['Phone Number'], unique_id=row['unikey'], First_Round_Interviewer_Name=row['1st  Round Interviewer Name'], Second_Round_Interviewer_Name=row['2nd Round Interviewer Name'],
                                        Third_Round_Interviewer_Name=row['Third Round Interviewer Name '], Management_Round_Interviewer_Name=row['Management/HR Round Interviewer Name'], HR_Round_Interviewer_Name=row['HR Round '])
            p.save()      


@authentication_classes([])
@permission_classes([]) 
class GetSupportData(APIView):
    def get(self,request,num):
        text_list=get_seoul_youth_list(num)
        #Support.objects.get_or_create(title=text_list[0],start_date=parse(text_list[1]),end_date=parse(text_list[2]),organizer=text_list[4],qualifications=text_list[5])


        return Response({"success":True})



'''

@authentication_classes([])
@permission_classes([]) 
class GetSupportData(APIView):
    def post(self,request):
        query=request.data['query']
        #text_list=get_seoul_youth_list(num)
        xml_data=get_youth_center(query)
        #Support.objects.get_or_create(title=text_list[0],start_date=parse(text_list[1]),end_date=parse(text_list[2]),organizer=text_list[4],qualifications=text_list[5])

        dict_type = xmltodict.parse(xml_data)
        json_type = json.dumps(dict_type)
        dict2_type = json.loads(json_type)
        return Response(dict2_type['empsInfo']['emp'])


@authentication_classes([])
@permission_classes([]) 
class SearchSupportData(APIView):
    def post(self,request):
        query=request.data['query']
        #text_list=get_seoul_youth_list(num)
        #Support.objects.get_or_create(title=text_list[0],start_date=parse(text_list[1]),end_date=parse(text_list[2]),organizer=text_list[4],qualifications=text_list[5])

        dict2_type=get_youth_center(query)
        support_dict=dict2_type['empsInfo']['emp']
    
        support_dict=dict2_type['empsInfo']['emp']
        support_serializers=OpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))  
        if (support_serializers.is_valid()):
            #불필요한 데이터 쌓임 방지
            #support_serializers.save()
            pass
        else:
            print(support_serializers.errors)
        return Response(support_serializers.data)


@authentication_classes([])
@permission_classes([]) 
class SmartRecommendSupportData(APIView):
    def post(self,request):
        query=request.data['query']
        member_id=request.data.get('member_id','')
        detail_field=request.data.get('detail_field','6')
        home_field=request.data.get('home_field','')
        job=request.data.get('job','')
        #text_list=get_seoul_youth_list(num)
        #Support.objects.get_or_create(title=text_list[0],start_date=parse(text_list[1]),end_date=parse(text_list[2]),organizer=text_list[4],qualifications=text_list[5])

        result_list=[]
        #1번 검색
        if (detail_field=='1'):
            query['query']="다자녀"
        elif (detail_field=='2'):
            query['query']="한부모"
        elif (detail_field=='3'):
            query['query']="다문화"
        elif (detail_field=='4'):
            query['query']="군인"
        elif (detail_field=='5'):
            query['query']="다자녀"
        else:
            pass
        
        dict2_type=get_youth_center(query)
        support_dict=dict2_type['empsInfo']['emp']
        for i in support_dict:
            i['member_id']=member_id
            i['detail_field']=detail_field
        support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))
        if (support_serializers.is_valid()):
            #불필요한 데이터 쌓임 방지
                #support_serializers.save()
            #print(support_serializers.data)
            result_list.append(support_serializers.data)
        


        #디테일 필드 검색 
  
        print(dict2_type)
        if (home_field=='1'):
            query['query']="기숙사"
            dict2_type=get_youth_center(query)
            print(dict2_type)
            support_dict=dict2_type['empsInfo']['emp']
            for i in support_dict:
                i['member_id']=member_id
                i['detail_field']=detail_field
            support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))
            if (support_serializers.is_valid()):
                #불필요한 데이터 쌓임 방지
                    #support_serializers.save()
                #print(support_serializers.data)
                result_list.append(support_serializers.data)

            query['query']="자취"
            dict2_type=get_youth_center(query)
            print(dict2_type)
            support_dict=dict2_type['empsInfo']['emp']
            for i in support_dict:
                i['member_id']=member_id
                i['detail_field']=detail_field
            support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))
            if (support_serializers.is_valid()):
                #불필요한 데이터 쌓임 방지
                    #support_serializers.save()
                #print(support_serializers.data)
                result_list.append(support_serializers.data)

        if (job=="학생"):
            query['query']="학생"
        elif (job=="직장인"):
            query['query']="직장인"     
        elif (job=="프리랜서"):
            query['query']="프리랜서"    
 
        dict2_type=get_youth_center(query)
        support_dict=dict2_type['empsInfo']['emp']
        try:

            for i in support_dict:
                i['member_id']=member_id
                i['detail_field']=detail_field
            support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))
            if (support_serializers.is_valid()):
                #불필요한 데이터 쌓임 방지
                #support_serializers.save()
                #print(support_serializers.data)
                result_list.append(support_serializers.data)
                #print(result_list)
            else:
                print(support_serializers.errors)
            return Response(result_list)
        except Exception as e:
            print(e)
            pass
            return Response([])

@authentication_classes([])
@permission_classes([]) 
class SmartRecommendDevelopSupportData(APIView):
    #serializers=SmartOpenapiSupportSerializer
    def post(self,request):
        query=request.data['query']
        detail_field=request.data.get('detail_field','6')
        member_id=request.data.get('member_id','')
        home_field=request.data.get('home_field','')
        job=request.data.get('job','')
        location=request.data.get('location','')
        location_numbering={"서울":"003002001","부산":"003002002","대구":"003002003","인천":"003002004","광주":"003002005",
        "대전:":"003002006","울산":"003002007","경기":"003002008","강원":"003002009","충북":"003002010","충남:":"003002011",
        "전북":"003002012","전남":"003002013","경북":"003002014","경남":"003002015","제주":"003002016","세종":"003002017"

        }
        #text_list=get_seoul_youth_list(num)
        #Support.objects.get_or_create(title=text_list[0],start_date=parse(text_list[1]),end_date=parse(text_list[2]),organizer=text_list[4],qualifications=text_list[5])
        try:
            query['srchPolyBizSecd']=location_numbering[location]
            #print(query['srchPolyBizSecd'])
        except:
            pass
        print(query)
        result_list=[]
        #1번 검색
        if (detail_field=='1'):
            query['query']="취약"
        elif (detail_field=='2'):
            query['query']="다자녀"
        elif (detail_field=='3'):
            query['query']="다문화"
        elif (detail_field=='4'):
            query['bizTycdSel']="004006"
        elif (detail_field=='5'):
            query['query']="장애"
        else:
            pass
        
        dict2_type=get_youth_center(query)
        print(dict2_type)
        if (dict2_type['empsInfo']['totalCnt']=="1"):
            support_dict=dict2_type['empsInfo']['emp']
            support_dict['member_id']=member_id
            support_dict['detail_field']=detail_field
            support_dict['job_info']=job
            support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(dict2_type,list))
            if (support_serializers.is_valid()):
                result_list.append(support_serializers.data)
            else:
                print(support_serializers.errors)
        elif (dict2_type['empsInfo']['totalCnt']=="0"):
            pass
        else:
            support_dict=dict2_type['empsInfo']['emp']
            for i in support_dict:
                i['member_id']=member_id
                i['detail_field']=detail_field
                i['job_info']=job
            support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))
            if (support_serializers.is_valid()):
                #불필요한 데이터 쌓임 방지
                    #support_serializers.save()
                for i in support_serializers.data:
                        result_list.append(i)
        

        
        

        #디테일 필드 검색 

        
  
        if (home_field=='1'):
            query['query']="기숙사"
            dict2_type=get_youth_center(query)
            print(dict2_type)

                
            if (dict2_type['empsInfo']['totalCnt']=="1"):
                support_dict=dict2_type['empsInfo']['emp']
                support_dict['member_id']=member_id
                support_dict['detail_field']=detail_field
                support_dict['job_info']=job
                support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(dict2_type,list))
                if (support_serializers.is_valid()):
                    result_list.append(support_serializers.data)
                    print(result_list)
                else:
                    print(support_serializers.errors)
            elif (dict2_type['empsInfo']['totalCnt']=="0"):
                pass
            else:
                support_dict=dict2_type['empsInfo']['emp']

                for i in support_dict:
                    i['member_id']=member_id
                    i['detail_field']=detail_field
                    i['job_info']=job
                support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))
                if (support_serializers.is_valid()):
                    #불필요한 데이터 쌓임 방지
                        #support_serializers.save()
                    for i in support_serializers.data:
                            result_list.append(i)

        if (job=="대학생"):
            query['query']="대학"
        elif (job=="직장인"):
            query['query']="직장"     
        elif (job=="프리랜서"):
            query['query']="자영업"    
 
        dict2_type=get_youth_center(query)
        print(dict2_type)
        print("query",query)
        
        try:
            if (dict2_type['empsInfo']['totalCnt']=="1"):
                support_dict=dict2_type['empsInfo']['emp']
                support_dict['member_id']=member_id
                support_dict['detail_field']=detail_field
                support_dict['job_info']=job
                support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(dict2_type,list))
                if (support_serializers.is_valid()):
                    result_list.append(support_serializers.data)
                    print(result_list)

            elif (dict2_type['empsInfo']['totalCnt']=="0"):
                pass
            else:
                support_dict=dict2_type['empsInfo']['emp']

                for i in support_dict:
                    i['member_id']=member_id
                    i['detail_field']=detail_field
                    i['job_info']=job
                support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))
                if (support_serializers.is_valid()):
                    #불필요한 데이터 쌓임 방지
                        #support_serializers.save()
                    for i in support_serializers.data:
                            result_list.append(i)
                else:
                    print("123")
                    print(support_serializers.errors)
            #return Response(result_list)
        except Exception as e:
            print(e)
            
            pass
        random_list=random.sample(result_list, 6)
        support_serializers=SmartOpenapiCreateSupportSerializer(data=random_list, many=isinstance(support_dict,list))
        if (support_serializers.is_valid()):
                #불필요한 데이터 쌓임 방지
                #support_serializers.save()
                print(support_serializers.data)
        else:
                print(support_serializers.errors)
        #QR코드 생성 및 QR코드 return 
        return Response(support_serializers.data)
        
        

@authentication_classes([])
@permission_classes([]) 
class CategorylistView(APIView):
    def post(self,request):
        plcyTpNm=request.data['plcyTpNm']
        category=request.data['category']
        color=request.data['color']
        supports = Support.objects.filter(plcyTpNm=plcyTpNm).distinct()
        #즐겨찾기 연결 -> 몇개 나오게 할 건지, 생각!!!!
        #SupportBookMark.objects.create
        data = list(supports.values())
        try:
            for i in data:
                try:
                    Category.objects.get_or_create(support_id=Support.objects.get(uuid=i['uuid']),colored=color,category=category)
                except:
                    print("!23")
            return Response({"success":True})
        except Exception as e:
            print(e)
            return Response({"success":False})





@authentication_classes([])
@permission_classes([])
class ChannelsandSupportListnameview(APIView):
    def get(self, *args, **kwargs):
        if (kwargs['name']=="channel"):
            status = Channel.objects.all()
            status_kind = status.values('channel_name').distinct().order_by('-channel_name')
            print(status_kind)
            return Response(status_kind)
        else:
            status = Category.objects.all()
            status_kind = status.values('category').distinct().order_by('-category')
            print(status_kind)
            return Response(status_kind)


    



@authentication_classes([])
@permission_classes([])
class GetSmartDetailRecommendView(APIView):
    def post(self,request,*args, **kwargs):
        detail_field=request.data.get('detail_field','6')
        member_id=request.data.get('member_id','')
        home_field=request.data.get('home_field','')
        job=request.data.get('job','')
        in_progress=request.data.get('in_progress','')
        location=request.data.get('location','')

        location_numbering={"서울":"003002001","부산":"003002002","대구":"003002003","인천":"003002004","광주":"003002005",
        "대전:":"003002006","울산":"003002007","경기":"003002008","강원":"003002009","충북":"003002010","충남:":"003002011",
        "전북":"003002012","전남":"003002013","경북":"003002014","경남":"003002015","제주":"003002016","세종":"003002017"

        }
        query=''
    
        query=query+"&srchRegion="+location_numbering[location]

        if (detail_field=='2'):
             query+="&srchWord=다자녀"
        elif (detail_field=='1'): #취약계층
            query+="&srchSpecField=007003"
        elif (detail_field=='3'): #군인
            query+="&srchWord=군인"
            query+="&srchSpecField=007006"
            
        elif (detail_field=='4'): #코로나19
             query+="&srchPlcyTp=004006"
        elif (detail_field=='5'): #장애우
             query+="&srchWord=장애"
             query+="&srchSpecField=007004"
        else:
            pass

        if (job=="대학생"):
            query+="&srchEmpStatus=006003"
        elif (job=="직장인"):
            query+="&srchEmpStatus=006001"
        elif (job=="프리랜서"):
            query+="&srchEmpStatus=006006"
        elif (job=="자영업자"):
            query+="&srchEmpStatus=006002"
        else:
            pass
    
        if (in_progress=="재학생"):
            query+="&srchEdubg=012005"
        elif (in_progress=="석/박사"):
            query+="&srchEdubg=012008"
        else:
            pass


        URL = f"https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?&bizId=&chargerOrgCdAll=&dtlOpenYn=Y&srchTermMm6=&frameYn=&pageIndex=1&pageUnit=24"+query
        website = requests.get(URL)

        soup = BeautifulSoup(website.text,"html.parser")
    

        #chrome_options = Options()
        #chrome_options.add_argument( '--headless' )
        #chrome_options.add_argument( '--log-level=3' )
        #chrome_options.add_argument( '--disable-logging' )
        #chrome_options.add_argument( '--no-sandbox' )
        #chrome_options.add_argument( '--disable-gpu' )

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        #chrome_options.headless = True
        #driver = webdriver.Chrome(executable_path="/Users/heejeong/gitkraken/molmot-backend-app/molmot_server/chromedriver",chrome_options=chrome_options)
        driver = webdriver.Chrome(executable_path="/home/ubuntu/molmot-backend-app/molmot_server/chromedriver",chrome_options=chrome_options)
        driver.implicitly_wait(3)
        
        driver.get( URL )
        driver.execute_script("f_srch();")
        #driver.execute_script("f_srch();")
        #driver.execute_script("fn_move(6);")
        driver.implicitly_wait(2)
        html = driver.page_source
        #print(html)
        soup = BeautifulSoup(html,"html.parser")

        notice=soup.find("div",class_="sch-result-wrap compare-result-list")

        notice=soup.find("div",class_="result-list-box")

        #location=soup.find("div",class_="badge").get_text()
        try:
            location=soup.find("span",class_="grey-label").get_text()
        except:
            pass
        result_data=[]
        try:
            notice.find("ul").find_all('li')
        except AttributeError: 
            return Response([])
        for i in notice.find("ul").find_all('li'):
            #print(i.find("a")["id"])
            supports_list=i.find("a")["id"][8:]
        
            jv_script="f_Detail('"+supports_list+"');"
            print(jv_script)
            query={
                "openApiVlak":"167693bf2984bec5368623af",
                "display":1,
                "pageIndex":1
            }
            query['srchPolicyId']=supports_list
            dict2_type=get_youth_center(query)
            support_dict=dict2_type['empsInfo']['emp']
            support_dict['member_id']=member_id
            support_dict['detail_field']=detail_field
            support_dict['job_info']=job
            support_dict['in_progress']=in_progress
            support_serializers=SmartOpenapiSupportSerializer(data=support_dict, many=isinstance(support_dict,list))
        
            if support_serializers.is_valid():
                    result_data.append(support_serializers.data)
            else:
                print(support_serializers.errors)
                pass
        print(URL)
        try:
            random_list=random.sample(result_data, 6)
            support_serializers=SmartOpenapiCreateSupportSerializer(data=random_list, many=isinstance(random_list,list))
            if (support_serializers.is_valid()):
                    #불필요한 데이터 쌓임 방지
                    #support_serializers.save()
                    #print(support_serializers.data)
                    pass
            else:
                    print(support_serializers.errors)
            #QR코드 생성 및 QR코드 return 
            return Response(support_serializers.data)
        except:
            support_serializers=SmartOpenapiCreateSupportSerializer(data=result_data, many=isinstance(result_data,list))
            if (support_serializers.is_valid()):
                    pass
                    #불필요한 데이터 쌓임 방지
                    #support_serializers.save()
                    #print(support_serializers.data)
            else:
                    print(support_serializers.errors)
            return Response(support_serializers.data)
        
        
    def get(self,*args, **kwargs):
        #URL = f"https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?_csrf=d852c94c-4a08-449a-925f-fc961f296287&bizId=&chargerOrgCdAll=&dtlOpenYn=Y&frameYn=&pageIndex=1&pageUnit=12&plcyTpOpenTy=&srchAge=&srchEdubg=012008&srchEmpStatus=006001"
        
        URL = f"https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do?_csrf=fa5d6b34-d414-4313-aa2f-96b63ed6d934&srchRegion=003002001&srchEmpStatus=006005&bizId=&chargerOrgCdAll=&dtlOpenYn=Y&srchTermMm6=&frameYn=&pageIndex=1&pageUnit=12&plcyTpOpenTy=list_004004&srchEdubg=012008"
        website = requests.get(URL)

        soup = BeautifulSoup(website.text,"html.parser")
    

        chrome_options = Options()
        chrome_options.add_argument( '--headless' )
        chrome_options.add_argument( '--log-level=3' )
        chrome_options.add_argument( '--disable-logging' )
        chrome_options.add_argument( '--no-sandbox' )
        chrome_options.add_argument( '--disable-gpu' )
        
        driver = webdriver.Chrome('/home/ubuntu/molmot-backend-app/molmot_server/chromedriver',chrome_options=chrome_options)
        driver.implicitly_wait(3)
        driver.get( URL )
        driver.execute_script("f_srch();")
        #driver.execute_script("f_srch();")
        #driver.execute_script("fn_move(6);")
        driver.implicitly_wait(2)
        html = driver.page_source
        #print(html)
        soup = BeautifulSoup(html,"html.parser")

        notice=soup.find("div",class_="sch-result-wrap compare-result-list")
        print(notice)
        notice=soup.find("div",class_="result-list-box")
        print(notice)
        #location=soup.find("div",class_="badge").get_text()
        try:
            location=soup.find("span",class_="grey-label").get_text()
        except:
            pass
        result_data=[]
        for i in notice.find("ul").find_all('li'):
            print(i.find("a")["id"])
            supports_list=i.find("a")["id"][8:]
        
            jv_script="f_Detail('"+supports_list+"');"
            print(jv_script)
            query={
                "openApiVlak":"167693bf2984bec5368623af",
                "display":1,
                "pageIndex":1
            }
            query['srchPolicyId']=supports_list
            dict2_type=get_youth_center(query)
            support_dict=dict2_type['empsInfo']['emp']
            support_serializers=OpenapiSupportSerializer(data=support_dict, many=isinstance(dict2_type,list))
        
            if support_serializers.is_valid():
                    result_data.append(support_serializers.data)
            else:
                pass
        
        return Response({"success":result_data,"len": len(notice.find("ul").find_all('li'))})
        