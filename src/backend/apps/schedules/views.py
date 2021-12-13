from django.contrib.messages.api import error
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, request
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.core.models import Room, Campus, Workstation
from apps.schedules.models import LabPetition, Module, Event, ModuleEvent
from apps.schedules.forms import LabPetitionForm, ModuleForm
from datetime import date, timedelta, datetime
import time 

# Create your views here.

def salas(request):
    template_name="salas.html"
    context={}
    laboratories=Room.objects.all()
    modulevent=ModuleEvent.objects.all()
    context['laboratories']=laboratories
    context['modulevent']=modulevent
    return render(request, template_name, context)

def calendario(request, id):
    template_name="calendario.html"
    context={}
    room = Room.objects.get(id = id)
    modulevent=ModuleEvent.objects.filter()
    context['modulevent']=modulevent
    context['room']=room
    return render(request, template_name, context)

def moduleconfig(request):
    template_name = "moduleconfig.html"
    context = {}
    context['moduledata'] = Module.objects.all().order_by('resume_module')
    moduleform= ModuleForm(request.POST or None)
    if request.method == 'POST':
        if moduleform.is_valid():
            moduleform.save()
            return HttpResponseRedirect(reverse('moduleconfig'))
    context['moduleform'] = moduleform
    return render(request, template_name, context)

def deletemodule(request, id):
    template_name = "moduleconfig.html"
    context = {}
    Module.objects.filter(id=id).delete()
    return render(request, template_name, context)

def administrar(request):
    template_name="administrar.html"
    context = {}
    context['labpetition'] = LabPetition.objects.all()
    context['modules'] = Module.objects.all()
    return render(request, template_name, context)

def reserve_event(petition):
    
    event_obj = Event.objects.create(name=petition.name_petition, labpetition=petition)
    date_start = petition.date_start_petition
    date_finish = petition.date_finish_petition
    weekDay = petition.day_petition
    modules = Module.objects.filter(start_module__range=(petition.time_start_petition,petition.time_finish_petition)).order_by('start_module')
    event_dates = [date_start + timedelta(days=x) for x in range((date_finish-date_start).days + 1) if (date_start + timedelta(days=x)).weekday() == time.strptime(weekDay, '%w').tm_wday]
    module_events = []
    for ed in event_dates:
        for m in modules:
           module_events.append(ModuleEvent(event=event_obj, module=m, day=ed))
    print(module_events)
    ModuleEvent.objects.bulk_create(module_events)
    
    return False
    

def administrarid(request, id):
    template_name="administrarid.html"
    context={}
    labid=LabPetition.objects.get(id = id)
    if request.method == 'GET':
        form_lab=LabPetitionForm(instance = labid)
        context['formlab']=form_lab
    else:
        form_lab=LabPetitionForm(request.POST, instance = labid)
        if form_lab.is_valid():
                       
            reserve_event(labid)
            form_lab.save()
            #return HttpResponseRedirect(reverse('administrar'))
        print(form_lab.errors)
    context['formlab']=form_lab
    return render(request, template_name, context)

def moduleid(request, id):
    template_name="moduleid.html"
    modid=Module.objects.get(id = id)
    context={}
    if request.method == 'GET':
        form_module=ModuleForm(instance = modid)
        context['formmodule']=form_module
    else:
        form_module=ModuleForm(request.POST, instance = modid)
        if form_module.is_valid():
            form_module.save()
            return HttpResponseRedirect(reverse('moduleconfig'))
    context['formmodule']=form_module
    return render(request, template_name, context)

def reservar(request):
    template_name="reservar.html"
    context={}
    context['modules'] = Module.objects.all()
    form_lab=LabPetitionForm(request.POST or None, prefix='formlab')
    if request.method == 'POST':
        if form_lab.is_valid():
            form_lab.save()
            return HttpResponseRedirect(reverse('salas'))
    context['formlab']=form_lab
    return render(request, template_name, context)

