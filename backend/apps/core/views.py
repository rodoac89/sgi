from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import Campus

@login_required
def index(request):
    template_name = "index.html"
    context = {}    
    if request.method == 'POST':        
        form = Campus(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/saludo/')
    else:
        form = Campus()
        context['formulario'] = form
    return render(request, template_name, context)


def dashboard(request):
    template_name = "dashboard.html"
    context={}
    context['num_lab'] = 'A1 COM301'
    context['cant_pc'] = 48
    context['exp_lic'] = 3
    context['active_lic'] = 10
    context['mant_pc'] = 5
    return render(request, template_name, context)

    

