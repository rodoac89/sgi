from django.shortcuts import render
from .utils import getSessionsByOption, formatSessions

def index(request):
    sessions = getSessionsByOption('today')
        
    return render(request, 'sessions.html', {
        'sessions': formatSessions(sessions)
    })
