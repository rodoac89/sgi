from django import forms
from django.forms import fields, ModelForm
from .models import LicensesList, SoftwareForm

class SoftwareRequestForm(forms.ModelForm):
    class Meta:
        model = SoftwareForm
        fields = ('name_user','last_name','rut','email','subject','nrc','software_name','software_type', 'room_name','details')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder' : ''
                }
            )
        }
        labels = {
            'status' : 'Estado',
            'name_user' : 'Nombres',
            'last_name' : 'Apellidos',
            'rut' : 'Rut',
            'email' : 'Email',
            'subject' : 'Asignatura',
            'nrc' : 'Nrc',
            'software_name' : 'Software',
            'software_type' : 'Tipo',
            'room_name' : 'Laboratorio',
            'details' : 'Detalles a destacar',
        }


class EnterLicensesForm(forms.ModelForm):
    class Meta:
        model = LicensesList
        fields = '__all__'
        widgets = {
            'license_due_date': forms.DateInput(
                attrs={
                    'type' : 'date'
                }
            )
        }
        labels = {
            'license_name' : 'Nombre de la licencia',
            'license_type' : 'Tipo de licencia',
            'license_stock' : 'Cantidad de licencias',
            #'license_in_use' : 'Cantidad en uso',
            'license_due_date' : 'Fecha de caducidad',
        }




    """id_request = forms.AutoField(primary_key=True)
    creation_date = forms.DateField('Creation date', auto_now = True, auto_now_add = False)
    name_user = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    rut = forms.CharField(max_length=10)
    email = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=100)
    nrc = forms.CharField(max_length=8)
    software_name = forms.CharField(max_length=100)
    details = forms.CharField(max_length=330)"""


