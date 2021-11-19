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
from apps.schedules.models import LabPetition, modulepetition, module
from apps.schedules.forms import LabPetitionForm, ModulePetitionForm

# Create your views here.

def salas(request):
    template_name="salas.html"
    context={}
    laboratories=Room.objects.all()
    campus=Campus.objects.all()
    labpetition=LabPetition.objects.filter(status_petition='P')
    module=modulepetition.objects.all()
    context['laboratories']=laboratories
    context['campus']=campus
    context['labpetition']=labpetition
    context['module']=module
    return render(request, template_name, context)

def calendario(request):
    template_name="calendario.html"
    context={}
    #context['name'] = request.GET['name']
    return render(request, template_name, context)

def reserva(request):
    template_name="reserva.html"
    context={}
    #context['name'] = request.GET['name']
    return render(request, template_name, context)

def administrar(request):
    template_name="administrar.html"
    context={}
    labpetition=LabPetition.objects.all()
    modpetition=modulepetition.objects.all()
    context['labpetition']=labpetition
    context['modpetition']=modpetition
    return render(request, template_name, context)

def administrarid(request, id):
    template_name="administrarid.html"
    labid=LabPetition.objects.get(id = id)
    modpetition=modulepetition.objects.filter(labpetition_mp=labid)
    print(labid)
    print(modpetition)
    context={}
    if request.method == 'GET':
        form_lab=LabPetitionForm(instance = labid)
        form_mod=ModulePetitionForm(instance = modpetition)
        context['formlab']=form_lab
        context['formmod']=form_lab
    else:
        form_lab=LabPetitionForm(request.POST, instance = labid)
        form_mod=ModulePetitionForm(request.POST, instance = modpetition)
        if form_lab.is_valid() and form_mod.is_valid():
            lab=form_lab.save()
            mod=form_mod.save()
            mod.labpetition_mp = lab
            mod.save()
            return HttpResponseRedirect(reverse('administrar'))
        print(form_lab.errors)
        print(form_mod.errors)
    context['formlab']=form_lab
    context['formmod']=form_mod
    return render(request, template_name, context)

def reservar(request):
    template_name="reservar.html"
    context={}
    form_lab=LabPetitionForm(request.POST or None, prefix='formlab')
    form_mod=ModulePetitionForm(request.POST or None, prefix='formmod')
    if request.method == 'POST':
        print(form_mod)
        if form_mod.is_valid() and form_lab.is_valid():
            lab=form_lab.save()
            mod=form_mod.save()
            mod.labpetition_mp = lab
            mod.save()
            return HttpResponseRedirect(reverse('administrar'))
        else:
            context['formmod']=form_mod
            context['formlab']=form_lab
        print(form_lab.errors)
        print(form_mod.errors)
    if request.method == 'GET':
        context['formmod']=form_mod
        
    context['formlab']=form_lab
    context['formmod']=form_mod
    return render(request, template_name, context)
