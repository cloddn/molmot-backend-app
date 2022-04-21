from rest_framework import serializers

from support.models import Support,Subscribe,SupportNotification


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('__all__')

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('__all__')


class SupportNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportNotification
        fields = ('__all__')