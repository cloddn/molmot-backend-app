from django.shortcuts import render
from rest_framework import generics
from media.models import UIPhoto

from media.serializers import UIPhotoSerializer
from rest_framework.decorators import permission_classes, authentication_classes


@authentication_classes([])
@permission_classes([]) 
class HomeLoadImageView(generics.ListAPIView):
    serializer_class = UIPhotoSerializer

    def get_queryset(self):
        field = self.kwargs['field']
        indexnum = self.kwargs['index']
        return UIPhoto.objects.filter(field=field,indexnum=indexnum)