from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.models import Campus, Room, Workstation
from django.contrib.auth.models import User


def index(request):
    template_name = "index.html"
    context={}
    
    try:
        user = User.objects.get(pk=1)
        return redirect('login')
    except:
        return redirect('wizard')
    

@login_required
def dashboard(request):
    template_name = "dashboard.html"
    context={}
    camupuses= Campus.objects.all()
    context['camupuses'] = camupuses
    if camupuses.count() == 0:
        context['msg'] = "Comienza registrando algunos laboratorios desde tu panel de administración"
    return render(request, template_name, context)


@login_required
def viewroom(request, room):
    template_name = "viewroom.html"
    context={}
    context['room'] = Room.objects.get(id=room) 
    
        
    return render(request, template_name, context)

        
def wizard(request):
    if request.POST:
        
        User.objects.create_superuser(request.POST["username"], request.POST["email"], request.POST["password"])
        import json
        data = json.load(request.FILES["backupdata"])
        for d in data:
            campus = Campus.objects.create()
            campus.name = name=d['campus']['name']
            campus.location_latitude = name=d['campus']['latitude']
            campus.location_longitude = name=d['campus']['longitude']
            campus.active = name=d['campus']['active']
            campus.inactive_by = name=d['campus']['inactive_by']
            campus.save()
            
            for r in d['campus']['rooms']:
                room = Room.objects.create()
                room.room_name = r['room_name']
                room.campus = campus
                room.address = r['address']
                room.active = r['active']
                room.inactive_by = r['inactive_by']
                room.save()
                for pc in range(r['cant_pc']):
                    workstation = Workstation.objects.create()
                    workstation.name = r['room_name'] + "PC" + ( ("0"+ str(pc+1)) if pc+1 < 10 else str(pc+1))
                    workstation.monitor_inches = 15
                    workstation.room = room
                    workstation.save()
                else:
                    workstation = Workstation.objects.create()
                    workstation.name = r['room_name'] + "PCProfesor"
                    workstation.monitor_inches = 15
                    workstation.room = room
                    workstation.save()
                    
        return redirect('index')
    template_name="wizard.html"
    context={}
    
    
    return render(request, template_name, context)

    




