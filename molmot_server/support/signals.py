from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.db.models import signals
from django.dispatch import receiver


from support.models import Support, SupportBookMark,SupportNotification,SupportScheduledNotification
import json
import datetime
from django_celery_beat.models import CrontabSchedule, PeriodicTask,IntervalSchedule

from user.models import MemberFCMDevice

#@receiver(signals.post_save, sender=Support) #Support 정보 수정하면 -> SupportNotification 수정하기.
#def run_task_on_Support_save(sender, instance, created, **kwargs):
    #if (created==False):
        #try:
            #신청 날짜 지나면 마감 하루 일자 하루전 , 안지났으면 시작 일자 7일 동안 울리게 
        #    sched_noti=SupportNotification.objects.filter(pk=instance.pk).update(
        #            noti_on_time=instance.start_date,
        #            crontab=instance.start_date
        #            )
        #except SupportNotification.DoesNotExist:
        #    pass


#즐겨찾기 수정됐을때가 있나....?즐겨찾기 삭제될경우 -> 없어져야함.
@receiver(signals.post_save, sender=SupportBookMark) #즐겨찾기한 지원금 제도에 한정해서 추가되도록 
def run_task_on_SupportBookMark_save(sender, instance, created, **kwargs):
    if (created):
        try:
            #신청 날짜 지나면 마감 하루 일자 하루전 , 안지났으면 시작 일자 7일 동안 울리게 
            #기기 토큰 1개만 가지고 있을 수 있도록...?
            support_id=Support.objects.get(uuid=instance.support_id.pk)
            member_device_info=MemberFCMDevice.objects.get(user=instance.member_id)
            interval=IntervalSchedule.objects.get_or_create(every="7",period="days")[0]
            SupportNotification.objects.get_or_create(
                member_device_info=member_device_info,
                support_id=support_id,
                noti_on_time=datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,17,00),
                interval=interval,
                last_run_at=datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,17,00),
                start_time=datetime.datetime(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day,17,00),
                name=str(member_device_info.user)+"의 지원금"+support_id.title+"알림",          
                task='support.tasks.support_notification_push',
                kwargs=json.dumps({'support_id':str(support_id.uuid),'member_id':str(instance.member_id)}))
        except Support.DoesNotExist or MemberFCMDevice.DoesNotExist:
            pass


@receiver(signals.post_delete, sender=SupportBookMark) #즐겨찾기한 지원금 제도에 한정해서 추가되도록 
def run_task_on_SupportBookMark_deleted_save(sender, instance, **kwargs):
        try:
            #신청 날짜 지나면 마감 하루 일자 하루전 , 안지났으면 시작 일자 7일 동안 울리게 
            #기기 토큰 1개만 가지고 있을 수 있도록...?
            support_id=Support.objects.get(uuid=instance.support_id.pk)
            member_device_info=MemberFCMDevice.objects.get(user=instance.member_id)
            SupportNotification.objects.filter(
                name=str(member_device_info.user)+"의 지원금"+support_id.title+"알림",          
                task='support.tasks.support_notification_push').delete()
        except Support.DoesNotExist or MemberFCMDevice.DoesNotExist:
            pass




