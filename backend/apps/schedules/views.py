from django.contrib.messages.api import error
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, request
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from apps.core.models import Room, Campus
from apps.schedules.models import LabPetition, modulepetition
from apps.schedules.forms import LabPetitionForm, modulepetitionForm

# Create your views here.

def salas(request):
    template_name="salas.html"
    context={}
    laboratories=Room.objects.all()
    campus=Campus.objects.all()
    context['laboratories']=laboratories
    context['campus']=campus
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
    context['labpetition']=labpetition
    return render(request, template_name, context)

def administrarid(request, id):
    template_name="administrarid.html"
    labid=LabPetition.objects.get(id = id)
    context={}
    if request.method == 'GET':
        form_lab=LabPetitionForm(instance = labid)
        context['formlab']=form_lab
    else:
        form_lab=LabPetitionForm(request.POST, instance = labid)
        if form_lab.is_valid():
            form_lab.save()
            return HttpResponseRedirect(reverse('administrar'))
    return render(request, template_name, context)

def reservar(request):
    template_name="reservar.html"
    context={}
    if request.method == 'POST':
        formlab=LabPetitionForm(request.POST, prefix='formlab')
        formmod=modulepetitionForm(request.POST, prefix='formmod')
        if formmod.is_valid() and formlab.is_valid():
            lab=formlab.save()
            mod=formmod.save()
            mod.labpetition_module = lab
            mod.save()
            return HttpResponseRedirect(reverse('administrar'))
        else:
            context['formmod']=formmod
            context['formlab']=formlab
        print(formlab.errors)   
    else:
        context['formlab']=LabPetitionForm()
        context['formmod']=modulepetitionForm()
    return render(request, template_name, context)