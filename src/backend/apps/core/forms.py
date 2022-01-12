from django import forms
from django.forms import fields
from . import models

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    rut = forms.CharField(label='RUT', max_length=100)

class Campus(forms.ModelForm):
    class Meta:
        model = models.Campus
        fields = ['name', 'location_latitude', 'location_longitude']
