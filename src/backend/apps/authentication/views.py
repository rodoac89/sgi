from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse

def login_view(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index')) 
    
    context = {}
    template_name = 'login.html'
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            context['error'] = "Usuario o contraseña incorrecta"
    return render(request, template_name, context)


def logout_view(request):
    context = {}
    template_name = 'login.html'
    logout(request)
    return render(request, template_name, context)