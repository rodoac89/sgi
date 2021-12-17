from django import forms
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, EmailField, DateTimeField
from django.forms import fields
from datetime import date, datetime
from django.forms import widgets
from django.forms.forms import Form
from django.forms.widgets import DateInput, EmailInput, TimeInput
from apps.schedules.models import LabPetition, Module
from apps.core.models import Room
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
            'date_start_petition',
            'date_finish_petition',
            'time_start_petition',
            'time_finish_petition',
            'day_petition',
            'recurrence',
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
            'date_start_petition':'Fecha inicio:',
            'date_finish_petition':'Fecha termino:',
            'time_start_petition':'Hora inicio:',
            'time_finish_petition':'Hora termino:',
            'day_petition':'Día:',
            'recurrence':'Recurrencia:',
            'memo_petition':'Mensaje:',
            'status_petition':'Status:',
        }

        widgets={
            'email_petition':EmailInput(attrs={}),
            'date_start_petition':DateInput(attrs={'id':'kt_datepicker_7', 'data-date-format':'dd/mm/yyyy', 'readonly':'readonly'}),
            'date_finish_petition':DateInput(attrs={'id':'kt_datepicker_7', 'data-date-format':'dd/mm/yyyy', 'readonly':'readonly'}),
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
        self.fields['date_start_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['date_finish_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['time_start_petition'] = forms.ChoiceField(choices=[(o.start_module, str(o)) for o in Module.objects.all().order_by('start_module')])
        self.fields['time_finish_petition'] = forms.ChoiceField(choices=[(o.finish_module, str(o)) for o in Module.objects.all().order_by('start_module')])
        self.fields['time_start_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['time_finish_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['day_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['recurrence'].widget.attrs.update({'class':'form-control'})
        self.fields['memo_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['status_petition'] = forms.ChoiceField(choices=([('A', 'Aceptado'),('R', 'Rechazado'),('P', 'Pendiente')]), required=False)
        self.fields['status_petition'].widget.attrs.update({'class':'form-control'})
        self.fields['date_start_petition'].input_formats=[ '%d/%m/%Y' ]
        self.fields['date_finish_petition'].input_formats=[ '%d/%m/%Y' ]


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [ 
            'resume_module',
            'name_module',
            'start_module',
            'finish_module',
        ]
        labels = {
            'resume_module':'Identificador',
            'name_module':'Nombre',
            'start_module':'Hora de inicio',
            'finish_module':'Hora de termino',
        }
        widgets={
            'start_module':TimeInput(attrs={'id':'kt_timepicker_5'}),
            'finish_module':TimeInput(attrs={'id':'kt_timepicker_5'}),
        }
    def __init__(self,*args, **kwargs):
        super(ModuleForm, self).__init__(*args,**kwargs)
        self.fields['resume_module'].widget.attrs.update({'class':'form-control'})
        self.fields['name_module'].widget.attrs.update({'class':'form-control'})
        self.fields['start_module'].widget.attrs.update({'class':'form-control'})
        self.fields['finish_module'].widget.attrs.update({'class':'form-control'})
