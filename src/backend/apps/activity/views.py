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
    first_room_id = rooms.first()["id"]
    workstations = getLatestSessions(first_room_id)

    return render(request, "current_state.html", {
        "campuses": campuses,
        "rooms": rooms,
        "workstations": workstations
    })

def getLatestSessions(room):
    workstations = Workstation.objects.filter(room_id=room)
    
    latest_sessions = {}
    for workstation in workstations:
        latest_session = Session.objects.filter(workstation=workstation).order_by("start").values().last()
        if latest_session is not None:
             latest_session["start"] = formatTimestamp(latest_session["start"])
             if latest_session["end"] is not None:
                 latest_session["end"] = formatTimestamp(latest_session["end"])
            
        latest_sessions[workstation.name] = latest_session

    return latest_sessions