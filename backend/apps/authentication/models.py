from django.db import models
from django.contrib.auth.models import User as auth_user
from datetime import datetime
import os


def photo_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "photo.%s" % (ext)
    path = "core/profile/"+instance.user.username
    path_to_file = os.path.join(path, filename)

    return path_to_file


def get_date():
    return datetime.now().strftime("%Y%m%d%H%M%S")


class Role(models.Model):
    role_name = models.CharField(max_length=50, default="Rol")
    weight = models.IntegerField()
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(auth_user, on_delete=models.CASCADE)
    image_profile = models.ImageField(
        upload_to=photo_file_name, null=True, blank=True)
    since = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)