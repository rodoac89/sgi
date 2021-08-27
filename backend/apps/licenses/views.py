"""from django.http import HttpResponseRedirect, request
"""
from django.shortcuts import render



def home(request):
    return render(request,'index.html')


def formulario(request):
    return render(request,'formulario.html')

def labs(request):
    return render(request,'visualizar_labs.html')

def adm_licencias(request):
    return render(request,'administrar_licencias.html')

def equipos(request):
    return render(request,'visualizar_equipos.html')    

def pc(request):
    return render(request,'pc.html')        