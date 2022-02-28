from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.models import Campus, Room, Workstation
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def admin_campus(request):
    template_name = "admin/campus.html"
    context={}
    camupuses= Campus.objects.all()
    context['camupuses'] = camupuses
    context['msg'] = ""
    if camupuses.count() == 0:
        if not request.user.is_admin:
            context['msg'] = "Solicita al administrador que registre Campus para continuar"
        else:
            context['msg'] = "Comienza registrando algunos laboratorios desde tu panel de administración"
    return render(request, template_name, context)

@login_required
def admin_users(request):
    template_name = "admin/user_management.html"
    context={}
    users= User.objects.all().order_by('id')
    context['users'] = users

    return render(request, template_name, context)

@login_required
def add_campus(request):
    if request.POST:
        Campus.objects.create(name=request.POST['campusname'])
    
    return redirect("admin_campus")

@login_required
def add_room(request, campus):
    if request.POST:
        Room.objects.create(room_name=request.POST['roomname'], campus=Campus.objects.get(id=campus), address=request.POST['roomaddress'])
    
    return redirect("admin_campus")

@login_required
def add_masive_workstations(request, room):
    if request.POST:
        r = Room.objects.get(id=room)
        for pc in range(int(request.POST['cant_pc'])):
            Workstation.objects.create(
                name = r.room_name + "PC" + ( ("0"+ str(pc+1)) if pc+1 < 10 else str(pc+1)),
                pc_model = request.POST['pc_model'],
                processor_model = request.POST['processor_model'],
                ram_capacity = request.POST['ram_capacity'],
                disk_capacity = request.POST['disk_capacity'],
                monitor_model = request.POST['monitor_model'],
                monitor_inches = int(request.POST['monitor_inches']),
                room = r
            )
    
    return redirect("admin_campus")

