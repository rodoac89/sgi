from django import forms
from .models import ScheduledReview

class ScheduledReviewForm(forms.ModelForm):
    class Meta:
        model = ScheduledReview
        fields = '__all__'
        date_scheduled = forms.DateField(input_formats=['%d/%m/%Y'])
        labels = {

            'date_scheduled':'Fecha a programar',
            'title':'Título de la revisión',
            'room':'Seleccione el laboratorio a revisar',

        }
        widgets = {

            'date_scheduled' : forms.DateInput(attrs={'class': 'form-control datetimepicker-input','data-target': '#datetimepicker1'}),
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'room': forms.Select(attrs={'class':'form-control'})

        }
      
