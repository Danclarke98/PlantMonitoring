from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Device(models.Model):
    device_id = models.IntegerField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.device_id)


class Data(models.Model):

    device = models.ForeignKey(Device, to_field='device_id', on_delete=models.CASCADE)
    temp = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    water = models.IntegerField(default=0)
    date_posted = models.DateTimeField()


class ACL(models.Model):

    username = models.TextField()
    topic = models.TextField()
