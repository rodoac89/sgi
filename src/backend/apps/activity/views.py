from django.shortcuts import render
from apps.core.models import Campus, Room, Workstation
from apps.activity.models import Session
from .utils import getSessionsByOption, formatSessions, formatTimestamp

def index(request):
    sessions = getSessionsByOption("today")
    campuses = Campus.objects.all().values()
    first_campus_id = campuses.first()["id"]
    rooms = Room.objects.all().values()
    first_room_id = rooms.first()["id"]
    workstations = getWorkstations(first_campus_id, first_room_id)
        
    return render(request, "index.html", {
        "campuses": campuses,
        "rooms": rooms,
        "workstations": workstations,
        "sessions": formatSessions(sessions)
    })

def state(request):
    campuses = Campus.objects.all().values()
    first_campus_id = campuses.first()["id"]
    rooms = Room.objects.all().values()
    first_room_id = rooms.first()["id"]
    workstations = getLatestSessions(first_campus_id, first_room_id)

    return render(request, "current_state.html", {
        "campuses": campuses,
        "rooms": rooms,
        "workstations": workstations
    })

def getWorkstations(campus, room):
    workstations = Workstation.objects.filter(
        room_id=room,
        room__campus_id=campus
    ).values()
    return workstations

def getLatestSessions(campus, room):
    workstations = Workstation.objects.filter(
        room_id=room,
        room__campus_id=campus
    )
    
    latest_sessions = {}
    for workstation in workstations:
        latest_session = Session.objects.filter(pc=workstation).order_by("start").values().last()
        if latest_session is not None:
             latest_session["start"] = formatTimestamp(latest_session["start"])
             if latest_session["end"] is not None:
                 latest_session["end"] = formatTimestamp(latest_session["end"])
            
        latest_sessions[workstation.name] = latest_session

    return latest_sessions