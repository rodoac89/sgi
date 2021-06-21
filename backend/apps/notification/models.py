from django.db import models
from django.contrib.auth.models import User as dj_user


class Notif(models.Model):
    user = models.ForeignKey(dj_user, on_delete=models.CASCADE)
    message = models.TextField(default="")
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    url = models.URLField(max_length=200, blank=True)
