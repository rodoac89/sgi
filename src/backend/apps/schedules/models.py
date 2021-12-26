import django
from django.db import models
from django.contrib.auth.models import User as auth_user
from apps.core.models import Workstation, Room
from datetime import datetime, timedelta

class RoomPetition(models.Model):
    STATUS = (
        ('P','Pendiente'),
        ('A','Aceptada'),
        ('R','Rechazada'),
    )
    DAY = (
        ('1','Lunes'),
        ('2','Martes'),
        ('3','Miercoles'),
        ('4','Jueves'),
        ('5','Viernes'),  
        ('6','Sabado'),
        ('0','Domingo'),
    )
    RECURRENCE = (
        ('07','Semanal'),
        ('01','Diario'),
        ('28','Mensual'),
    )
    TYPE = (
        ('N','Normal'),
        ('E','Extraordinario'),
    )
    event_petition = models.CharField(max_length=30, default="")
    name_petition = models.CharField(max_length=50, default="")
    email_petition = models.CharField(max_length=50, default="")
    room_petition = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    computer_petition = models.IntegerField(default="")
    date_start_petition = models.DateField(null=True)
    date_finish_petition = models.DateField(null=True)
    day_petition = models.CharField(max_length=1, choices=DAY, default="1")
    time_start_petition = models.TimeField(null=True)
    time_finish_petition = models.TimeField(null=True)
    recurrence = models.CharField(max_length=2, choices=RECURRENCE, default='07')
    memo_petition = models.CharField(max_length=100, default="", null=True)
    type_petition = models.CharField(max_length=1, choices=TYPE, default="N")
    status_petition = models.CharField(max_length=1, choices=STATUS, default="P", null=True)
    datetime_petition = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.name_petition, self.room_petition)

class Module(models.Model):
    resume_module = models.CharField(max_length=50, default="")
    name_module = models.CharField(max_length=50, default="")
    start_module = models.TimeField(null=True)
    finish_module = models.TimeField(null=True)
    
    def __str__(self):
        return "{} : {} - {}".format(self.name_module, self.start_module, self.finish_module)

class Event(models.Model):    
    name_event = models.CharField(max_length=50)
    roompetition_event = models.ForeignKey(RoomPetition, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name_event)

class ModuleEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    day = models.DateField(auto_now=False)
    
#class Event(models.Model):
#    name_event = models.CharField(max_length=20, default="", blank=True)
#    day_event = models.ForeignKey(DayPetition, on_delete=models.SET_NULL, null=True, blank=True)
#    module_event = models.ForeignKey(Module, on_delete=models.SET_NULL,null=True, blank=True)

#class Schedule(models.Model):
#    lab_schedule = models.ForeignKey(RoomPetition, on_delete=models.SET_NULL,null=True, blank=True)
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

