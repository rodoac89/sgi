from django.db import models
from django.contrib.auth.models import User as dj_user
from datetime import datetime
import os


def photo_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "photo.%s" % (ext)
    path = "core/profile/"+instance.user.username
    path_to_file = os.path.join(path, filename)

    return path_to_file

# TODO: Crear realicion de jerarquia y relacion de adminsitracion de labs


class Role(models.Model):
    role_name = models.CharField(max_length=50, default="Role")
    weight = models.IntegerField()
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(dj_user, on_delete=models.CASCADE)
    image_profile = models.ImageField(
        upload_to=photo_file_name, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
