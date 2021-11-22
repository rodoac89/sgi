from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.models import Room


@login_required
def dashboard(request):
    template_name = "dashboard.html"
    context={}
    rooms= Room.objects.all()
    context['rooms'] = rooms
    print(rooms)
    return render(request, template_name, context)

def load(request):
    from django.contrib.auth.models import User
    user = User.objects.create_user(username='labs',
                                 email='',
                                 password='1234')
    return redirect('dashboard')

