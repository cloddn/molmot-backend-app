from django.shortcuts import render
from django.urls import path,include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from .views import *
from rest_framework.routers import DefaultRouter

from user import views

#ViewSet을 이용한 라우팅 방식 이용 
router = DefaultRouter()
router.register('profile', views.ProfileViewSet)

urlpatterns = [
    
    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),

    path('create', Registration.as_view()),
    path('login', Login.as_view()),
    path('auth/',AuthSMSAPI.as_view()),
    path('auth/?phone_number=<str:phone_number>&auth_number=<int:auth_number>',AuthSMSAPI.as_view()),
    path('idpw-check/',IDPWCheckingAPI.as_view()),
    path('idpw-check/?phone_number=<str:phone_number>&auth_number=<str:auth_number>',IDPWCheckingAPI.as_view()),
    #path('user-info-view/',UserInfoView.as_view()),
    #path('user-info-view/<uuid:userid>/',UserInfoView.as_view()),


]

urlpatterns += router.urls