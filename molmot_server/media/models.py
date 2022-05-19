from django.db import models
import uuid

from user.models import Member

class UIPhoto(models.Model):
    FIELD = (    #홈배너 이용
        ('banner', 'banner'), #현재 사용
        ('notice', 'notice '), #사용 X
    )
    title=models.TextField(null=True)
    body=models.TextField(null=True)
    field=models.CharField(verbose_name='field',max_length=10,choices=FIELD,null=True)
    indexnum=models.IntegerField(unique=True,null=True) #index 1만 쓰고 있음
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo_file=models.ImageField(upload_to='ui-photo') #홈 배너 이미지 필드
    def __str__(self):
        return str(self.indexnum)



class SmartResultQRPhoto(models.Model):
    member_id=models.ForeignKey(Member,null=True,on_delete=models.CASCADE)
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo_file=models.ImageField(upload_to='qr-code-photo') #홈 배너 이미지 필드
    def __str__(self):
        return str(self.member_id)