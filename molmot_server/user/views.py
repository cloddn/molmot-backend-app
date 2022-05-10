from pickle import TRUE
import re
from xxlimited import Null
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

from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import viewsets



# 누구나 접근 가능
@permission_classes([AllowAny]) 
class Registration(generics.GenericAPIView):
    serializer_class = CustomRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        if serializer.is_valid():
            user = serializer.save(request) # request 필요 -> 오류 발생
            return Response(
                {
                # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
                # 디폴트 정보 context는 request, view, format
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data
                },
                    status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
                # 디폴트 정보 context는 request, view, format
                    "success":False
                },
                    status=status.HTTP_400_BAD_REQUEST,
            )


@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
    
        if user['email'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)
        

    
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data, 
                "token": user['token'],
                "logined":user['logined']
            }
        )


@permission_classes([AllowAny])
class AuthSMSAPI(APIView):
    def post(self, request):#인증 번호 요청
        try:
            p_num = request.data['phone_number']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            AuthSMS.objects.update_or_create(phone_number=p_num)
            return Response({'message': 'OK','timestamp':str(int(time.time() * 1000))})

    def get(self,request): #인증 완료 
        p_num=request.query_params['phone_number']
        a_num=request.query_params['auth_number']
        result=AuthSMS.check_auth_number(AuthSMS.objects.get(phone_number=p_num),p_num,a_num)
        return Response({'message': 'OK','timestamp':str(int(time.time() * 1000)),'result':result})

@permission_classes([AllowAny])
class IDPWCheckingAPI(APIView): #아이디 알려주기 
    def post(self, request):
        try:
            if request.data.get('new_pw',None)!=None:
                email = request.data['email']
                member_obj=Member.objects.get(email=email)
                member_obj.set_password(request.data['new_pw'])
                member_obj.save()
                return Response({'message': 'OK','timestamp':str(int(time.time() * 1000)),'result':request.data['new_pw']}, status=status.HTTP_200_OK)
            else:
                p_num=request.query_params['phone_number']
                a_num=request.query_params['auth_number']
                result=AuthSMS.check_auth_number(AuthSMS.objects.get(phone_number=p_num),p_num,a_num)
                if (result==True):
                    return Response({'message': 'OK','timestamp':str(int(time.time() * 1000))}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError or Member.DoesNotExist:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            p_num=request.query_params['phone_number']
            a_num=request.query_params['auth_number']
            result=AuthSMS.check_auth_number(AuthSMS.objects.get(phone_number=p_num),p_num,a_num)
            memberid=Member.objects.get(phone_number=p_num)
            return Response({'message': 'OK','timestamp':str(int(time.time() * 1000)),'result':memberid.email},status=status.HTTP_200_OK)
        except KeyError or Member.DoesNotExist:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([]) 
@permission_classes([]) 
class UserInfoView(APIView):
    @login_check
    def get(self,request,userid):
        try:
            user_id = request.user.uuid
            userinfo=UserSerializer(Member.objects.get(uuid=user_id))
            return Response({'user_info':userinfo.data})
        except:
            return Response({'user_info':'fail'})
    @login_check
    def get(self,request):
        user_id = request.user.uuid
        userinfo=UserSerializer(Member.objects.get(uuid=user_id))
        return Response({'user_info':userinfo.data})

#데코레이터 안되는 문제 해결하기 
#@login_check([])
@authentication_classes([])
@permission_classes([]) 
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if self.kwargs.get('member_id',None)!=None:
            member_id=self.kwargs.get('member_id',None)
            return super().get_queryset().filter(member_id=member_id)
        else:
            return super().get_queryset()


import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
 
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
@authentication_classes([])
@permission_classes([]) 
def Import_csv(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
          
            myfile = request.FILES['myfile']        
            empexceldata = pd.read_csv(myfile,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                 
                fromdate_time_obj = dt.datetime.strptime(dbframe.DOB, '%d-%m-%Y')
                obj = CityAddress.objects.create(city=dbframe.city,address=dbframe.address)
                print(type(obj))
                obj.save()
 
            return Response({"success":True})
    except Exception as identifier:            
        print(identifier)
     
    return Response({"success":False})