from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Campus(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    location_latitude = models.CharField(max_length=50, blank=True, null=True)
    location_longitude = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)
    deleted_by = models.TextField(default="", blank=True, null=True)
    deleted_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_name = models.CharField(max_length=50, blank=True, null=True)
    campus = models.ForeignKey(
        Campus, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    chief = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    deleted_by = models.TextField(default="")
    deleted_date = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return "{} - {}".format(self.campus.name, self.room_name)


class Workstation(models.Model):
    name = models.CharField(max_length=25)
    ip = models.CharField(max_length=50, blank=True, null=True)
    pc_model = models.CharField(max_length=50, blank=True, null=True)
    pc_serialnumber = models.CharField(max_length=50, blank=True, null=True)
    processor_model = models.CharField(max_length=50, blank=True, null=True)
    ram_capacity = models.CharField(max_length=50, blank=True, null=True)
    disk_type = models.CharField(max_length=50, blank=True, null=True)
    disk_capacity = models.CharField(max_length=50, blank=True, null=True)
    monitor_model = models.CharField(max_length=50, blank=True, null=True)
    monitor_serialnumber = models.CharField(
        max_length=15, blank=True, null=True)
    monitor_inches = models.PositiveIntegerField(default=0)
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=True)
    deleted_by = models.TextField(default="")
    deleted_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)
