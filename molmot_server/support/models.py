from pyexpat import model
from django.db import models
import uuid
# Create your models here.


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(
        max_length=50,
        null=False,
        unique=False
    )   
    location=models.CharField(
        max_length=50,
        null=True,
        unique=False,
        blank=True
    )   
    link=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.title

class Supports(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    title=models.CharField(
        max_length=50,
        null=False,
        unique=False
    )   
    detail=models.TextField()
    submit_link=models.URLField(blank=True,null=True)
    organizer=models.ForeignKey(Organization,null=True,on_delete=models.CASCADE)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    qualifications=models.TextField()

    def __str__(self):
        return self.title
