from django.contrib.messages.api import error
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, request
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from apps.core.models import Room, Campus, Workstation
from apps.schedules.models import LabPetition, modulepetition, Module
from apps.schedules.forms import LabPetitionForm, ModulePetitionForm, ModuleForm

# Create your views here.

def salas(request):
    template_name="salas.html"
    context={}
    laboratories=Room.objects.all()
    campus=Campus.objects.all()
    labpetition=LabPetition.objects.filter(status_petition='A')
    module=modulepetition.objects.all()
    context['laboratories']=laboratories
    context['campus']=campus
    context['labpetition']=labpetition
    context['module']=module
    return render(request, template_name, context)

def calendario(request, id):
    template_name="calendario.html"
    context={}
    room = Room.objects.get(id = id)
    labpetition = LabPetition.objects.filter(laboratory_petition = room)
    context['labpetition']=labpetition
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
            lab=form_lab.save()
            return HttpResponseRedirect(reverse('administrar'))
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
