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

def saludo(request):
    template_name="saludo.html"
    context={}
    #context['name'] = request.GET['name']
    return render(request, template_name, context)