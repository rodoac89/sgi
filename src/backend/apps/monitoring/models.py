from django.db import models
from datetime import datetime
import os

from django.utils import tree
from apps.core.models import Workstation, Room
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model

dj_user = get_user_model()

class Externuser (models.Model):
    email = models.EmailField(unique=True,max_length=60,blank=False,null=False)

    def __str__(self):
        return self.email

class TicketReport(models.Model):
    STATE_TICKET = [
        ('A', 'Abierto'),
        ('R', 'Revisando'),
        ('C', 'Cerrado')
        
    ]
    email = models.ForeignKey(Externuser,on_delete=models.SET_NULL,blank=True,null=True)
    pc = models.ForeignKey(Workstation,on_delete=models.SET_NULL,blank=True,null=True)
    category = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=1,blank=True,null=True,choices=STATE_TICKET,default='A')
    comment = models.CharField(max_length=200,blank=True,null=True)
    date_comment = models.DateTimeField(blank=True, null=True)
    user = user = models.ForeignKey(dj_user, on_delete=models.SET_NULL,blank=True,null=True)
    history = HistoricalRecords()
    def __str__(self):
        return "{} - {} - {}".format(self.pc,self.category,self.description)
    class Meta:
        ordering = ['-id']

class ScheduledReview(models.Model):
    date_scheduled = models.DateTimeField()
    title = models.CharField(max_length=50)
    room = models.ForeignKey(Room,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-id']    

class Revision (models.Model):
    Hardware_Revision = [
        ('P', 'Presenta'),
        ('NP', 'No Presenta'),
        ('D','Dañado')
    ]

    Software_SO_Revision = [
        ('O', 'Operativo'),
        ('F', 'Falla'),
        ('N', 'No Tiene')
    ]
    
    scheduled_review = models.ForeignKey(ScheduledReview,on_delete=models.SET_NULL,blank=True,null=True)
    pc = models.ForeignKey(Workstation,on_delete=models.SET_NULL,blank=True,null=True)
    monitor = models.CharField(max_length=2,null=False,blank=False,choices=Hardware_Revision,default="")
    mouse= models.CharField(max_length=2,null=False,blank=False,choices=Hardware_Revision,default="")
    keyboard= models.CharField(max_length=2,null=False,blank=False,choices=Hardware_Revision,default="")
    cpu = models.CharField(max_length=2,null=False,blank=False,choices=Hardware_Revision,default="")
    SO = models.CharField(max_length=2,null=False,blank=False,choices=Software_SO_Revision,default="")
    software = models.CharField(max_length=2,null=False,blank=False,choices=Software_SO_Revision,default="")
    observation = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(dj_user, on_delete=models.CASCADE,default="")

    def __str__(self):
        return "{} - {}".format(self.pc,self.observation)
