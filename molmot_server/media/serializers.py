from rest_framework import serializers
from .models import *


class UIPhotoSerializer(serializers.ModelSerializer):
    photo_file=serializers.SerializerMethodField()

    class Meta:
        model=UIPhoto
        fields=('__all__')


    def get_photo_file(self,data):
        return data.photo_file.url
    