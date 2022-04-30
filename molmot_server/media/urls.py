from django.urls import path
from .views import *
from . import views

urlpatterns=[
    path('home-load/<str:field>/<int:index>/',HomeLoadImageView.as_view()),
    path('home-ui-info-load/',GetHomeUIInfoView.as_view()),
    path('home-ui-info-load/<uuid:member_id>/',GetHomeUIInfoView.as_view()),
    
]