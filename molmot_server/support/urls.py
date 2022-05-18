
from django.shortcuts import render
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

from support import views



#ViewSet을 이용한 라우팅 방식 이용 
router = DefaultRouter()
router.register('support-notification', views.SupportNotificationViewSet)
router.register('subscribe', views.SubscribeViewSet)
router.register('channel', views.ChannelViewSet)
router.register('support-bookmark', views.SupportBookMarkViewSet)
#router.register('support-bookmark/<str:folder>/<uuid:member_id>', views.SupportBookMarkViewSet)
router.register('recording', views.RecordingListViewSet)


urlpatterns = [
    path('support-info-view/<uuid:support_id>/',SupportInfoView.as_view()),
    path('support-filter-view/',SupportFilterInfoView.as_view()),
    path('subscribe-info-view/<uuid:member_id>/',SubscribeInfoView.as_view()),
    path('support-all-alarms-off/<uuid:member_id>/<str:on_off>/',AllAlarmsONOFFView.as_view()),
    
    path('support-get-data/',GetSupportData.as_view()),
    path('support-search-data/',SearchSupportData.as_view()),
    path('support-smart-recommend-data/',SmartRecommendDevelopSupportData.as_view()),
    
    path('channels-get-list-view/',ChannelsView.as_view()),
    path('channels-get-list-view/<uuid:member_id>/',ChannelsView.as_view()),
    path('category-get-list-view/<str:colored>/',GetCategoryListView.as_view()),
   
    path('support-bookmark-list-create/', views.SupportBookMarkViewSet.as_view({'post': 'bookmark_list_create'}), name='bookmark_list_create'),
    path('support-bookmark-list-view/', views.SupportBookMarkViewSet.as_view({'get': 'bookmark_list'}), name='bookmark_list'),
    path('develop-category-create/',CategorylistView.as_view()),

    path('develop-channel-list-create/',SearchSupportData.as_view()),

    path('channel-support-name-list-get/<str:name>/',ChannelsandSupportListnameview.as_view()),
    ]


urlpatterns += router.urls