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

    def validate(self, data):
        try:
            Subscribe.objects.get(organizer_id=data['organizer_id'],member_id=data['member_id'])
            raise serializers.ValidationError(
                '이미 생성된 디비 입니다.'
            )
        except Subscribe.DoesNotExist:
            return data


class SupportNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportNotification
        fields = ('__all__')







'''
def create(self,validated_data):
        print("생성")
        group = Group.objects.create(**validated_data) 
        group.save()
        return group

    def update(self, instance, validated_data):
        group = Group.objects.get(pk=instance.uuid)
        Group.objects.filter(pk=instance.uuid)\
                           .update(**validated_data)
        return group
'''
