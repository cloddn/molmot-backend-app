from django.shortcuts import render
from django.urls import path
from .views import *

urlpatterns = [
    path('support-info-view/<uuid:support_id>/',SupportInfoView.as_view()),
    path('support-filter-view/',SupportFilterInfoView.as_view()),

    path('subscribe-info-view/<uuid:member_id>/',SubscribeInfoView.as_view()),

    
    
]
