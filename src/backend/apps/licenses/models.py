from django.db import models
from django.db.models.fields import CharField, DateField, AutoField

from apps.core.models import Room


software_form_status =[
    (1, 'No realizada'),
    (2, 'Realizada')
]


class TypeLicense(models.Model):
    type_name = models.TextField(default='')
    description = models.TextField(default='')

    class Meta:
        verbose_name = 'Tipo de licencia'
        verbose_name_plural = 'Tipo de licencia'

    def __str__(self):
        return self.type_name   
    
class SoftwareForm(models.Model):
    id_request = models.AutoField(primary_key=True)
    status = models.IntegerField(
        null=False, blank=False,
        choices = software_form_status,
        default= 2
    )
    creation_date = models.DateField('Creation date', auto_now = True, auto_now_add = False)
    name_user = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    rut = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    nrc = models.CharField(max_length=8)
    software_name = models.CharField(max_length=100)
    software_type = models.ForeignKey(TypeLicense, blank=True, null=True, on_delete=models.SET_NULL)
    room_name = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    details = models.CharField(max_length=330)

    class Meta:
        verbose_name = 'solicitud'
        verbose_name_plural = 'solicitudes'

    def __str__(self):
        return self.name_user

 

    

class LicensesList(models.Model):
    id_license = models.AutoField(primary_key=True)
    license_name = models.CharField(max_length=40)
    license_type = models.ForeignKey(TypeLicense, blank=True, null=True, on_delete=models.SET_NULL)
    license_stock = models.PositiveSmallIntegerField() 
    #license_in_use = models.PositiveSmallIntegerField()
    license_due_date = models.DateField()

    class Meta:
        verbose_name = 'license'
        verbose_name_plural = 'licenses'

    def __str__(self):
        return self.license_name
   