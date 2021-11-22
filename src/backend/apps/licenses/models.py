from django.db import models
from django.db.models.fields import CharField, DateField, AutoField


software_form_status =[
    (1, 'No realizada'),
    (2, 'Realizada')
]

software_form_type =[
    (1, 'Open Source'),   # Gratuita  
    # Pagadas o convenio
    (4, 'Estatica'),       # Por equipo
    (5, 'Flotante'),       # En el servidor
    (6, 'Fisica')         # Llave electronica

]

    
class SoftwareForm(models.Model):
    id_request = models.AutoField(primary_key=True)
    status = models.IntegerField(
        null=False, blank=False,
        choices = software_form_status,
        default= 1
    )
    creation_date = models.DateField('Creation date', auto_now = True, auto_now_add = False)
    name_user = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    rut = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    nrc = models.CharField(max_length=8)
    software_name = models.CharField(max_length=100)
    software_type = models.IntegerField(
        null=False, blank=False,
        choices = software_form_type,
        default= 1
    )
    details = models.CharField(max_length=330)

    class Meta:
        verbose_name = 'solicitud'
        verbose_name_plural = 'solicitudes'

    def __str__(self):
        return self.name_user

class TypeLicense(models.Model):
    type_name = models.TextField(default='Open source')
    description = models.TextField(default='')

    

class LicensesList(models.Model):
    id_license = models.AutoField(primary_key=True)
    license_name = models.CharField(max_length=40)
    license_type = models.ForeignKey(TypeLicense, blank=True, null=True, on_delete=models.SET_NULL)
    license_stock = models.PositiveSmallIntegerField() 
    license_in_use = models.PositiveSmallIntegerField()
    license_due_date = models.DateField()

    class Meta:
        verbose_name = 'license'
        verbose_name_plural = 'licenses'

    def __str__(self):
        return self.license_name
   