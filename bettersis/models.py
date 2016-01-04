from django.db import models
from django.utils import timezone

# Create your models here.

class Sitescope(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class MonitorCPU(models.Model):
    _id = models.CharField(max_length=100, unique=True, default=1)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    time = models.DateTimeField('time', default=timezone.now())
    value = models.FloatField(default=0)
    sitescope = models.ForeignKey(Sitescope)
    host = models.CharField(max_length=50)

    def __str__(self):
        return '{time}: {monitor} @ {host}'.format(time=self.time,
                                                   monitor=self.name,
                                                   host=self.host)

class MonitorMemory(models.Model):
    _id = models.CharField(max_length=100, unique=True, default=1)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    time = models.DateTimeField('time', default=timezone.now())
    value = models.FloatField(default=0)
    sitescope = models.ForeignKey(Sitescope)
    host = models.CharField(max_length=50)

    def __str__(self):
        return '{time}: {monitor} @ {host}'.format(time=self.time,
                                                   monitor=self.name,
                                                   host=self.host)

class Host(models.Model):
    name = models.CharField(max_length=200, unique=True)
    sitescope = models.ForeignKey(Sitescope)