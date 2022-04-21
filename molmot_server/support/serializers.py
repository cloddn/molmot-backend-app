from rest_framework import serializers

from support.models import Support,Subscribe


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('__all__')

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('__all__')


