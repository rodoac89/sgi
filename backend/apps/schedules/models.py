import django
from django.db import models
from django.contrib.auth.models import User as auth_user
from django.db.models.base import Model
from django.utils import timezone
from apps.core.models import Workstation, Room, Campus
from datetime import datetime, timedelta
import os

class LabPetition(models.Model):
    STATUS_PETITION = (
        ('P','Pendiente'),
        ('A','Aceptado'),
        ('R','Rechazado'),
    )
    name_petition = models.CharField(max_length=50, default="")
    email_petition = models.CharField(max_length=150, default="")
    nrc_petition = models.CharField(max_length=10, default="", blank=True)
    campus_petition = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True)
    laboratory_petition = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    cant_pc_petition = models.IntegerField(default="")
    day_start_petition = models.DateField(null=True)
    day_finish_petition = models.DateField(null=True)
    #time_start_petition = models.TimeField(null=True)
    #time_finish_petition = models.TimeField(null=True)
    memo_petition = models.CharField(max_length=250, default="", null=True)
    #license_petition = models.CharField(max_length=50, choices=licenses)
    status_petition = models.CharField(max_length=1, default="P", choices=STATUS_PETITION, blank=True)
    def __str__(self):
        return "{} - {} - {}".format(self.name_petition, self.campus_petition, self.laboratory_petition)

    def __unicode__(self):
        return "{} - {} - {}".format(self.name_petition, self.campus_petition, self.laboratory_petition)

class modulepetition(models.Model):
    MODULE = (
        ('1D','08:30-09:15'),
        ('2D','09:25-10:10'),
        ('3D','10:20-11:05'),
        ('4D','11:15-12:00'),
        ('5D','12:10-12:55'),
        ('6D','13:05-13:50'),
        ('7D','14:00-14:45'),
        ('8D','14:55-15:40'),
        ('9D','15:50-16:35'),
        ('10D','16:45-17:30'),
        ('11D','17:40-18:25'),
        ('12D','18:35-19:20'),
        ('13D','19:30-20:15'),
        ('14D','20:25-18:50'),
        ('1V','19:00-19:45'),
        ('2V','19:46-20:30'),
        ('3V','20:40-21:25'),
        ('4V','21:26-22:10'),
        ('5V','22:20-23:05'),
        ('6V','23:06-23:50'),
        ('7V','08:30-17:30'),
    )
    DAY = (
        ('LUN','Lunes'),
        ('MAR','Martes'),
        ('MIE','Miercoles'),
        ('JUE','Jueves'),
        ('VIE','Viernes'),
        ('SAB','Sabado'),
        ('DOM','Domingo'),
    )

    day_module = models.CharField(max_length=50, choices=DAY)
    start_module = models.CharField(max_length=50, choices=MODULE)
    finish_module = models.CharField(max_length=50, choices=MODULE)
    labpetition_module = models.ForeignKey(LabPetition, on_delete=models.SET_NULL, null=True, blank=True)
    

#class Event(models.Model):
#    name_event = models.CharField(max_length=20, default="", blank=True)
#    day_event = models.ForeignKey(DayPetition, on_delete=models.SET_NULL, null=True, blank=True)
#    module_event = models.ForeignKey(Module, on_delete=models.SET_NULL,null=True, blank=True)

#class Schedule(models.Model):
#    lab_schedule = models.ForeignKey(LabPetition, on_delete=models.SET_NULL,null=True, blank=True)
#    event_schedule = models.ForeignKey(Event, on_delete=models.SET_NULL,null=True, blank=True)
    


# class UserWortation(models.Model):
#     email = models.CharField(primary_key=True)
#     name = models.CharField(max_length=50, blank=True, null=True)
#     identifier = models.CharField(max_length=50, blank=True, null=True)


# class Subject(models.Model):
#     code = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)


# class Course(models.Model):
#     SHIFTS = (
#         ('D', 'Diurno'),
#         ('V', 'Vespertino'),
#     )
#     section = models.IntegerField()
#     code = models.IntegerField()
#     #period = foreign
#     shift = models.CharField(max_length=1, choices=SHIFTS)


# class ListCourse(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     user_worktation = models.ForeignKey(
#         UserWortation, on_delete=models.CASCADE)
