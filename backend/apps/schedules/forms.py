from django import forms
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, EmailField, DateTimeField
from django.forms import fields
from datetime import date, datetime
from django.forms import widgets
from django.forms.forms import Form
from django.forms.widgets import DateInput, EmailInput, TimeInput
from apps.schedules.models import LabPetition, modulepetition
from django.forms import ModelForm, Textarea

class LabPetitionForm(forms.ModelForm):
    class Meta:
        model = LabPetition
        fields = [
            'name_petition',
            'email_petition',
            'nrc_petition',
            'campus_petition',
            'laboratory_petition',
            'cant_pc_petition',
            'day_start_petition',
            'day_finish_petition',
            #'time_start_petition',
            #'time_finish_petition',
            'memo_petition',
            'status_petition',
        ]
        labels = {
            'name_petition':'Nombre:',
            'email_petition':'Email:',
            'nrc_petition':'NRC:',
            'campus_petition':'Sede:',
            'laboratory_petition':'Laboratorio:',
            'cant_pc_petition':'Computadores:',
            'day_start_petition':'Fecha inicio:',
            'day_finish_petition':'Fecha termino:',
            #'time_start_petition':'Hora inicio:',
            #'time_finish_petition':'Hora termino:',
            'memo_petition':'Mensaje:',
            'status_petition':'Status:',
        }

        widgets={
            'email_petition':EmailInput(attrs={}),
            'day_start_petition':DateInput(attrs={'id':'kt_datepicker_7', 'data-date-format':'dd/mm/yyyy', 'readonly':'readonly'}),
            'day_finish_petition':DateInput(attrs={'id':'kt_datepicker_7', 'data-date-format':'dd/mm/yyyy', 'readonly':'readonly'}),
            #'time_start_petition':TimeInput(attrs={'id':'kt_timepicker_5'}),
            #'time_finish_petition':TimeInput(attrs={'id':'kt_timepicker_5'}),
            'memo_petition':Textarea(attrs={'cols': 40, 'rows': 5})
        }

    def __init__(self,*args, **kwargs):
        super(LabPetitionForm, self).__init__(*args,**kwargs)
        self.fields['name_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['email_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['nrc_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['campus_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['laboratory_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['cant_pc_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['day_start_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['day_finish_petition'].widget.attrs.update({'class':'form-control'})
        #self.fields['time_start_petition'].widget.attrs.update({'class':'form-control'})
        #self.fields['time_finish_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['memo_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['status_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['day_start_petition'].input_formats=[ '%d/%m/%Y' ]
        self.fields['day_finish_petition'].input_formats=[ '%d/%m/%Y' ]

class modulepetitionForm(forms.ModelForm):
    class Meta:
        model = modulepetition
        fields = [ 
            'day_module',
            'start_module',
            'finish_module',
            'labpetition_module',
        ]
        labels = {
            'day_module':'Dia:',
            'start_module':'Modulo:',
            'finish_module':'Hasta el:',
        }
        widgets={

        }
    def __init__(self,*args, **kwargs):
        super(modulepetitionForm, self).__init__(*args,**kwargs)
        self.fields['day_module'].widget.attrs.update({'class':'form-control'})
        self.fields['start_module'].widget.attrs.update({'class':'form-control'})
        self.fields['finish_module'].widget.attrs.update({'class':'form-control'})