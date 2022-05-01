from cgitb import enable
import csv
import datetime
from pickle import TRUE
from re import L
from django.http import JsonResponse
from requests import api
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics # generics class-based view 사용할 계획

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes

# JWT 사용을 위해 필요
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from user.utils import login_check
from django.core import serializers as core_serializers

from .serializers import *
from .models import *
from rest_framework.views import APIView
from django.db.models import Q
import json
from django.utils.decorators import method_decorator
from rest_framework import viewsets

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
        return JsonResponse(data,safe=False)  
    
    
    def get(self,request,member_id):
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
                    
        supports = Support.objects.filter(q).order_by('-start_date')

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
        return JsonResponse(data,safe=False)  

@authentication_classes([]) 
@permission_classes([]) 
class SupportInfoView(generics.ListAPIView):
    serializer_class=SupportSerializer

    @login_check
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        support_id=self.kwargs['support_id']
        return Support.objects.filter(uuid=support_id)

@authentication_classes([]) 
@permission_classes([])
class SubscribeInfoView(generics.ListAPIView):
    serializer_class=SubscribeSerializer

    @login_check
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        member_id=self.kwargs['member_id']
        return Subscribe.objects.filter(member_id=member_id)





@authentication_classes([])
@permission_classes([]) 
class SupportNotificationViewSet(viewsets.ModelViewSet):
    queryset = SupportNotification.objects.all()
    serializer_class = SupportNotificationSerializer



from rest_framework import status, viewsets
from rest_framework.response import Response

@authentication_classes([])
@permission_classes([]) 
class SubscribeViewSet(viewsets.ModelViewSet):

    
    #I took the liberty to change the model to queryset
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer


    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
            if serializer.is_valid():
                headers = self.get_success_headers(serializer.data)
                return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([])
@permission_classes([]) 
class ChannelViewSet(viewsets.ModelViewSet):

    
    #I took the liberty to change the model to queryset
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
            if serializer.is_valid():
                headers = self.get_success_headers(serializer.data)
                return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({"success":False}, status=status.HTTP_400_BAD_REQUEST)



@authentication_classes([])
@permission_classes([]) 
class SupportBookMarkViewSet(viewsets.ModelViewSet):

    
    #I took the liberty to change the model to queryset
    queryset = SupportBookMark.objects.all()
    serializer_class = SupportBookMarkSerializer


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

'''
