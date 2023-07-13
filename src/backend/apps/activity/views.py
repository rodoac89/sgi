import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.core.models import Campus, Room, Workstation
from .utils import encryptAES

@login_required
def index(request):
    campuses = Campus.objects.all().values()
    if campuses:
        first_campus_id = campuses.first()["id"]
        rooms = Room.objects.filter(campus_id=first_campus_id).values()
        if rooms:
            first_room_id = rooms.first()["id"]
            workstations = workstations = Workstation.objects.filter(room_id=first_room_id).values()
        else:
            workstations = []
    else:
        rooms = []
        workstations = []
        
    return render(request, "index.html", {
        "campuses": campuses,
        "rooms": rooms,
        "workstations": workstations
    })

@login_required
def state(request):
    campuses = Campus.objects.all().values()
    if campuses:
        first_campus_id = campuses.first()["id"]
        rooms = Room.objects.filter(campus_id=first_campus_id).values()
    else:
        rooms = []
    adminEncrypted = encryptAES("iamadmin", os.getenv("WS_SECRET"))

    return render(request, "current_state.html", {
        "campuses": campuses,
        "rooms": rooms,
        "adminEncrypted": adminEncrypted
    })