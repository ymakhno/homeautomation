from datetime import timedelta
from django.db import models

# Create your models here.
class DeviceType:
    DIMMER = 0
    SWITCH = 1

class ZWaveApi(models.Model):
    url = models.CharField(max_length=255)

class Lighter(models.Model):
    name = models.CharField(max_length=255)
    access_name = models.CharField(max_length=255)
    lighter_type = models.IntegerField()
    internal_type = models.IntegerField()
    value = models.IntegerField(default=0)

    def is_dimmer(self):
        return self.lighter_type == DeviceType.DIMMER

    def internal_dimmer(self):
        return self.internal_type == DeviceType.DIMMER

    def __str__(self):
        return ("Lighter(name = '{self.name}', access_name = '{self.access_name}', "
                "lighter_type = {self.lighter_type}, internal_type = {self.internal_type}, value = {self.value})'").format(self=self)


class Rule(models.Model):
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    lighter = models.ForeignKey(Lighter)
    start = models.TimeField()
    start_delta = models.IntegerField()
    end = models.TimeField()
    end_delta = models.IntegerField()

    def check_day(self, date, check_end):
        days = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday]
        if check_end and self.end < self.start:
            date = date - timedelta(1)
        return days[date.weekday()]

    def __str__(self):
        days = [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday]
        return ("Rule(days = {days}, lighter = {self.lighter.id}, "
                "start = {self.start}, start_delta = {self.start_delta}, "
                "end = {self.end}, end_delta = {self.end_delta})").format(self = self, days = days)

class WebCamera(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    motion_control = models.BooleanField(default=False)