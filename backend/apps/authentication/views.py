from django.shortcuts import render

def login(request):
    context = {}
    template_name = 'login.html'
    render(request, template_name, context)
