from django.shortcuts import render
from rest_framework import generics
from media.models import UIPhoto

from media.serializers import UIPhotoSerializer



class HomeLoadImageView(generics.ListAPIView):
    serializer_class = UIPhotoSerializer

    def get_queryset(self):
        field = self.kwargs['field']
        indexnum = self.kwargs['index']
        return UIPhoto.objects.filter(field=field,indexnum=indexnum)