from django.forms import DateInput
from rest_framework import serializers

from support.models import Channel, Support,Subscribe,SupportNotification,SupportScheduledNotification
from user.models import Member
import datetime

class SupportSerializer(serializers.ModelSerializer):
    hits=serializers.SerializerMethodField()

    class Meta:
        model = Support
        fields = ('__all__')
    
    def get_hits(self,obj):
        obj.click
        return obj.hits

class HomeSupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Support
        fields = ('__all__')
    


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('__all__')

    def validate(self, data):
        try:
            sub_data,new=Subscribe.objects.get_or_create(organizer_id=data['organizer_id'],member_id=data['member_id'])
            return sub_data
        except:
            return data

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('__all__')

    def validate(self, data):
        try:
            ch_data,new=Channel.objects.get_or_create(organizer_id=data['organizer_id'],member_id=data['member_id'])
            Member.objects.get(uuid=data['member_id']).last_login=datetime.datetime.now()
            return ch_data
        except:
            return data


class SupportNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportNotification
        fields = ('__all__')

class SupportScheduledNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportScheduledNotification
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
