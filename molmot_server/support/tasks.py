import django
from celery.utils.log import get_task_logger
import datetime

from firebase_admin.messaging import AndroidConfig, Message, Notification
import datetime
from django.utils import timezone
from pytz import utc
import django
from firebase_admin import messaging
from firebase_admin.messaging import APNSFCMOptions, APNSPayload, Aps, ApsAlert, Message, Notification,APNSConfig

from support.models import Support, SupportNotification
from user.models import Member, MemberFCMDevice
logger = get_task_logger(__name__)

django.setup()

from celery import shared_task

@shared_task
def support_notification_push(*args, **kwargs):
   print("keyword args:", kwargs)
   #try:
   #except:
   print(kwargs)
   support_id=Support.objects.get(pk=kwargs['support_id'])
   member_id=Member.objects.get(pk=kwargs['member_id'])
   #d_day=str((support_id.end_date.date()-datetime.date.today()).days)
   #해당 서포트 아이디가 있는 사람에게 전송
   #registration_ja_tokens=list(SupportNotification.objects.filter(support_id=support_id).values_list('registration_id',flat=True))
   message=messaging.Message(android=AndroidConfig(priority="high"),apns=APNSConfig(payload=APNSPayload(aps=Aps(content_available=True,sound="default",badge=0))),notification=Notification(title=str(support_id.title),body="기간 정보를 알려드릴게요! "+support_id.date),token=MemberFCMDevice.objects.get(user=member_id).registration_id)
   response = messaging.send(message)
   print("푸시알림 정해진대로 전송")