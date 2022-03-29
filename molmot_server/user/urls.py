from django.shortcuts import render
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from .views import *

urlpatterns = [
    path('token/', obtain_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('token/refresh/', refresh_jwt_token),

    path('create', Registration.as_view()),
    path('login', Login.as_view()),
    path('auth/',AuthSMSAPI.as_view()),
    path('auth/?phone_number=<str:phone_number>&auth_number=<int:auth_number>',AuthSMSAPI.as_view()),
]