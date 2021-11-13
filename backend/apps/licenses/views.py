
"""from Labs.backend.apps.licenses.models import form_software"""
from apps.licenses.forms import SoftwareRequestForm, EnterLicensesForm
from django.http import HttpRequest
from django.shortcuts import render

from .models import LicensesList, SoftwareForm



def home(request):
    return render(request,'index.html')


#------FORMULARIOS------#

def form_index(request):
        form = SoftwareRequestForm()
        return render(request, "formulario.html", {"form":form})

def forms_view(request):
    context={}
    if request.GET:
        if 'id_user' in request.GET:
            data_forms = SoftwareForm.objects.get(id_request=int(request.GET['id_user']))
            context['formulario'] = data_forms

    return render(request, "solicitudes_software.html", context)

def form_info1(request):
    context={}
    if request.GET:
        if 'id_user' in request.GET:
            data_forms = SoftwareForm.objects.get(id_request=int(request.GET['id_user']))
            context['formulario'] = data_forms
    return render(request, "info_formulario1.html", context)   
    
def form_list(request):
    software_forms = SoftwareForm.objects.all()
    data = {
        'solicitudes': software_forms
    }
    return render(request,'listado_formularios.html', data)    

def form_info(request):
    software_forms = SoftwareForm.objects.all()
    data = {
        'solicitudes': software_forms
    }
    return render(request, "info_formulario.html", data)

def software_request_done(request):
    return render(request,'formulario_listo.html')

class SoftwareRequestView(HttpRequest):

    def form_create(request):
        form = SoftwareRequestForm()
        if request.method == 'POST':
            form = SoftwareRequestForm(request.POST)
            if form.is_valid():
                form.save()
                form = SoftwareRequestForm()
            context= {'form':form}    
                
        return render(request, 'formulario_listo.html', context)


#------LICENCIAS------#

def adm_licencias(request):
    licenses_lista = LicensesList.objects.all()
    data = {
        'listado_de_licencias': licenses_lista
    }
    return render(request,'listado_licencias.html', data)

def enter_licenses(request):
    license_form = EnterLicensesForm()
    return render(request, 'ingresar_licencia.html', {"license_form":license_form})    

class EnterLicensesView(HttpRequest):

    def enter_license(request):
        license_form = EnterLicensesForm()
        if request.method == 'POST':
            license_form = EnterLicensesForm(request.POST)
            if license_form.is_valid():
                license_form.save()
                license_form = EnterLicensesForm()
            context= {'license_form':license_form}    
                
        return render(request, 'licencia_lista.html', context)



def info_license(request):
    context={}
    if request.GET:
        if 'id_serch' in request.GET:
            data_forms = LicensesList.objects.get(id_license=int(request.GET['id_serch']))
            context['licencia'] = data_forms

    return render(request, "info_licencia.html", context)





#------EQUIPOS------#


def labs(request):
    return render(request,'visualizar_labs.html')

def equipos(request):
    return render(request,'visualizar_equipos.html')    

def pc(request):
    return render(request,'pc.html')        
