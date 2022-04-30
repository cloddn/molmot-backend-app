from django.urls import path
from .views import *
from . import views

urlpatterns=[
    path('home-load/<str:field>/<int:index>/',HomeLoadImageView.as_view()),
]