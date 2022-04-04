from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics # generics class-based view 사용할 계획
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes

# JWT 사용을 위해 필요
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .serializers import *
from .models import *
from rest_framework.views import APIView


# 누구나 접근 가능
@permission_classes([AllowAny]) 
class Registration(generics.GenericAPIView):
    serializer_class = CustomRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
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

@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
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
                "token": user['token']
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
        try:
            p_num=request.query_params['phone_number']
            a_num=request.query_params['auth_number']
            result=AuthSMS.check_auth_number(p_num,a_num)
            return Response({'message': 'OK','timestamp':str(int(time.time() * 1000)),'result':result})
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class IDPWCheckingAPI(APIView): #아이디 알려주기 
    def post(self, request):
        #try:
            p_num=request.query_params['phone_number']
            a_num=request.query_params['auth_number']
            email = request.data['email']
            member_obj=Member.objects.get(email=email)
            member_obj.set_password(request.data['new_pw'])
            member_obj.save()
            #result=AuthSMS.check_auth_number(AuthSMS.objects.get(phone_number=p_num),p_num,a_num)
            #if (authenticate(email=email,password=latest_pw)):
            return Response({'message': 'OK','timestamp':str(int(time.time() * 1000))}, status=status.HTTP_200_OK)
        #except KeyError:
        #    return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            p_num=request.query_params['phone_number']
            a_num=request.query_params['auth_number']
            result=AuthSMS.check_auth_number(AuthSMS.objects.get(phone_number=p_num),p_num,a_num)
            memberid=Member.objects.get(phone_number=p_num)
            return Response({'message': 'OK','timestamp':str(int(time.time() * 1000)),'result':memberid.email},status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


