from django.shortcuts import render
from apps.core.models import Campus, Room, Workstation
from apps.activity.models import Session
from .utils import formatTimestamp

def index(request):
    campuses = Campus.objects.all().values()
    first_campus_id = campuses.first()["id"]
    rooms = Room.objects.filter(campus_id=first_campus_id).values()
    first_room_id = rooms.first()["id"]
    workstations = workstations = Workstation.objects.filter(room_id=first_room_id).values()
        
    return render(request, "index.html", {
        "campuses": campuses,
        "rooms": rooms,
        "workstations": workstations
    })

def state(request):
    campuses = Campus.objects.all().values()
    first_campus_id = campuses.first()["id"]
    rooms = Room.objects.filter(campus_id=first_campus_id).values()

    return render(request, "current_state.html", {
        "campuses": campuses,
        "rooms": rooms
    })