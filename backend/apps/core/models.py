from django.db import models
from django.contrib.auth.models import User as auth_user
from datetime import datetime
import os


class Campus(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    location_latitude = models.CharField(max_length=50, blank=True, null=True)
    location_longitude = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)
    inactive_by = models.TextField(default="")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Room(models.Model):
    room_name = models.CharField(max_length=50, blank=True, null=True)
    campus = models.ForeignKey(
        Campus, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    inactive_by = models.TextField(default="")

    def __str__(self):
        return "{} - {}".format(self.campus.name, self.room_name)

    def __unicode__(self):
        return "{} - {}".format(self.campus.name, self.room_name)


class Workstation(models.Model):
    name = models.CharField(max_length=25)
    ip = models.CharField(max_length=15, blank=True, null=True)
    pc_model = models.CharField(max_length=15, blank=True, null=True)
    pc_serialnumber = models.CharField(max_length=15, blank=True, null=True)
    processor_model = models.CharField(max_length=15, blank=True, null=True)
    ram_capacity = models.CharField(max_length=15, blank=True, null=True)
    disk_type = models.CharField(max_length=15, blank=True, null=True)
    disk_capacity = models.CharField(max_length=15, blank=True, null=True)
    monitor_model = models.CharField(max_length=15, blank=True, null=True)
    monitor_serialnumber = models.CharField(
        max_length=15, blank=True, null=True)
    monitor_inches = models.PositiveIntegerField(default=0)
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)
    inactive_by = models.TextField(default="")

    def __str__(self):
        return "{}".format(self.name)

    def __unicode__(self):
        return "{}".format(self.name)


# Link user with workstation for labs for remote work

class UserWortation(models.Model):
    email = models.CharField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    identifier = models.CharField(max_length=50, blank=True, null=True)


class Subject(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class Course(models.Model):
    SHIFTS = (
        ('D', 'Diurno'),
        ('V', 'Vespertino'),
    )
    section = models.IntegerField()
    code = models.IntegerField()
    #period = foreign
    shift = models.CharField(max_length=1, choices=SHIFTS)


class ListCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_worktation = models.ForeignKey(
        UserWortation, on_delete=models.CASCADE)
