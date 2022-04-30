from rest_framework import serializers
from .models import *


class UIPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=UIPhoto
        fields=('__all__')