
"""from Labs.backend.apps.licenses.models import form_software"""
from datetime import datetime
from apps.licenses.forms import SoftwareRequestForm, EnterLicensesForm
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

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

def prueba(request):
    form = SoftwareRequestForm()
    return render(request,'formulario_copy.html', {"form":form})

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

def search_form(request):
    search = request.GET["buscar"]
    software_forms = SoftwareForm.objects.filter(name_user__icontains=search)
    context={
        'solicitudes':software_forms
    }
    # if search:
    #     licenses = LicensesList.objects.filter(
    #         Q(license_name__icontains = search),
    #         Q(license_type__icontains = search)
    #     ).distinct()

    return render(request,'listado_formularios.html', context)


    


def status_form(request, id):
    
    
    software_forms = get_object_or_404(SoftwareForm, id_request=id)
    data={
        'solicitudes': SoftwareForm.objects.all()
    }
    i = software_forms.status

    if request.method == 'POST':
        if i == 2:
            SoftwareForm.objects.filter(id_request=id).update(status=1)
            
            return render(request,'listado_formularios.html', data) 
        else: 
            SoftwareForm.objects.filter(id_request=id).update(status=2)
            
            return render(request,'listado_formularios.html', data)     

    return render(request, 'listado_formularios.html', data)




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



# def info_license(request):
#     context={}
#     if request.GET:
#         if 'id_serch' in request.GET:
#             data_forms = LicensesList.objects.get(id_license=int(request.GET['id_serch']))
#             context['licencia'] = data_forms
    

#     return render(request, "info_licencia.html", context)


def edit_license(request, id):

    license_form = get_object_or_404(LicensesList, id_license=id)

    data={
        'license_form' : EnterLicensesForm(instance=license_form)
    }

    data["info"]=id
    print(data)
    if request.method == 'POST':
        form = EnterLicensesForm(data=request.POST, instance=license_form)
        if form.is_valid():
            form.save()
            return redirect(to="licenses:adm_licencias")
        data["license_form"] = form   

    return render(request, 'editar_licencia.html', data)

def delete_license(request, id):

     license_form = get_object_or_404(LicensesList, id_license=id)   
     license_form.delete()
     return redirect(to='licenses:adm_licencias')

def search_license(request):
    search = request.GET["buscar"]
    listado_de_licencias = LicensesList.objects.filter(license_name__icontains=search)
    print(listado_de_licencias)
    context={
        'listado_de_licencias':listado_de_licencias
    }
    # if search:
    #     licenses = LicensesList.objects.filter(
    #         Q(license_name__icontains = search),
    #         Q(license_type__icontains = search)
    #     ).distinct()

    return render(request,'listado_licencias.html', context)


#------REPORTES------#

def reportes(request):
    return render(request, 'reportes1.html')

def licenses_reports(request):
    count_forms_request = []
    count_instalations_done = []
    count_licenses = []
    count_licenses_in_use = []
    count_licenses_in_use2 = []
    count_licenses_in_due = []
    date = datetime.today()
    year = date.strftime("%Y")
    begin = year+'-01-01'
    end = year+'-12-31'
    #------formularios------#
    form_reports = SoftwareForm.objects.filter(creation_date__range=(begin,end))     
    for r in form_reports:
        if r.id_request is not None:
            count_forms_request.append(1)
    form_reports1 = SoftwareForm.objects.filter(status=1)     
    for r in form_reports1:
        if r.id_request is not None:
            count_instalations_done.append(1)        
    c_formularios=sum(count_forms_request)   
    c_instalations=sum(count_instalations_done) 
    #------licencias------#
    licenses_reports = LicensesList.objects.all()     
    for r in licenses_reports:
        if r.id_license is not None:
            count_licenses.append(1)  
    licenses_reports1 = LicensesList.objects.all() 
    total_stock = 0
    for stock in licenses_reports1:
        total_stock += stock.license_stock
    
    c_licenses=sum(count_licenses)




    context={'c_formularios':c_formularios, 'c_instalations':c_instalations, 'c_licenses':c_licenses, 't_stock':total_stock, }    
    return render(request,'reportes.html', context)






#------EQUIPOS------#


def labs(request):
    return render(request,'visualizar_labs.html')

def equipos(request):
    return render(request,'visualizar_equipos.html')    

def pc(request):
    return render(request,'pc.html')        
