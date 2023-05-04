from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.db.models import Q
from apps.activity.models import Session
from apps.core.models import Workstation, Room, Campus
from apps.activity.utils import getSessionsBetweenTimestamps, getSessionsByOption, sessionsToJson, formatSessions
from datetime import datetime, time, timedelta

class Get(APIView):
    def get(self, request):
        gte = request.query_params.get('gte')
        lte = request.query_params.get('lte')
        option = request.query_params.get('option')
        if gte is not None and lte is not None:
            sessions = getSessionsBetweenTimestamps(gte, lte)
            if sessions is None:
                Response({'error': 'gte es mayor a lte'}, HTTP_400_BAD_REQUEST)
        elif option is not None:
            sessions = getSessionsByOption(option)
            if sessions is None:
                Response({'error': 'No existe la opción'}, HTTP_400_BAD_REQUEST)
        formattedSessions = formatSessions(sessions)
        return Response(sessionsToJson(formattedSessions), HTTP_200_OK)
    
class GetOptions(APIView):
    def get(self, request):
        campus = request.query_params.get("campus")
        room = request.query_params.get("room")
        
        if (campus is not None and not campus.isdigit()) or (room is not None and not room.isdigit()):
            return Response({"error": "Debe ingresar un campus y room válidos"},
                        status=HTTP_400_BAD_REQUEST)
        
        if campus is not None:
            rooms = Room.objects.filter(campus_id=campus).order_by("room_name").values()
        elif room is not None:
            roomObj = Room.objects.get(id=room)
            if not roomObj:
                return Response({"error": "No se encontró el room"},
                            status=HTTP_404_NOT_FOUND)
            campus = roomObj.campus     
            rooms = Room.objects.filter(campus=campus).order_by("room_name").values()
        
        if not rooms:
            return Response({"error": "No se encontraron rooms"},
                            status=HTTP_404_NOT_FOUND)
        
        if room is None:
            room = rooms[0]["id"]     
        
        workstations = Workstation.objects.filter(room_id=room).values()

        if not workstations:
            return Response({"error": "No se encontraron workstations."},
                        status=HTTP_404_NOT_FOUND)

        response = {
            "rooms": rooms,
            "workstations": workstations
        }

        return Response(response, HTTP_200_OK)

class GetChart(APIView):
    def post(self, request):
        campus = request.data.get('campus')
        room = request.data.get('room')
        ws = request.data.get('ws')
        ranges = request.data.get('ranges')

        if ranges is None or not ranges:
            return Response({'error': 'Parametros incorrectos.'},
                        status=HTTP_400_BAD_REQUEST)
        
        if (campus is not None and not campus.isdigit()) or (room is not None and not room.isdigit()) or (ws is not None and not ws.isdigit()):
            return Response({'error': 'Parametros incorrectos.'},
                        status=HTTP_400_BAD_REQUEST)
        
        # Se consultan las sesiones que tengan su inicio entre el inicio del primer rango y el fin del último rango.
        condition = (Q(start__gte = ranges[0][0]) & Q(start__lt = ranges[-1][1])) | (Q(end__gt = ranges[0][0]) & Q(end__lte = ranges[-1][1]))

        if ws is not None:
            condition &= Q(pc_id = ws)
        elif room is not None:
            condition &= Q(pc__room__id = room)
        elif campus is not None:
            condition &= Q(pc__room__campus__id = campus)
        
        sessions = Session.objects.filter(condition).order_by("start").values_list("start", "end")

        data = [0] * len(ranges) # array de ceros, donde se llenaran los valores para cada rango de tiempo.
        for session in sessions:
            sessionStart, sessionEnd = session
            sessionTime = sessionEnd - sessionStart
            for ranIndex in range(len(ranges)):
                rangeStart, rangeEnd = ranges[ranIndex]
                if (sessionStart >= rangeStart and sessionStart < rangeEnd):
                    currentEnd = min(sessionEnd, rangeEnd)
                    sessionRangeTime = currentEnd - sessionStart
                elif (sessionEnd > rangeStart and sessionEnd <= rangeEnd):
                    sessionRangeTime = sessionEnd - max(sessionStart, rangeStart)
                else:
                    continue

                data[ranIndex] += sessionRangeTime
                sessionTime -= sessionRangeTime
                if (sessionTime == 0):
                    break
                elif (sessionTime > 0):
                    sessionStart = rangeEnd

        return Response(data, HTTP_200_OK)
    
class GetCurrent(APIView):
    def get(self, request):
        campus = request.query_params.get('campus')
        room = request.query_params.get('room')
        if campus is None or not campus.isdigit() or (room is not None and not room.isdigit()):
            return Response({'error': 'Debe ingresar un campus y room válidos'},
                        status=HTTP_400_BAD_REQUEST)
        
        rooms = Room.objects.filter(campus_id=campus).order_by('room_name').values() 
        if room is None:            
            room = rooms.first()
            if room is None:
                return Response({'error': 'No se encontró room'},
                        status=HTTP_404_NOT_FOUND)
            room = room["id"]
        
        workstations = Workstation.objects.filter(
            room_id=room,
            room__campus_id=campus
        )

        if len(workstations) < 1:
            return Response({'error': 'No se encontro el campus y room consultados.'},
                        status=HTTP_404_NOT_FOUND)
        
        latest_sessions = {}
        for workstation in workstations:
            latest_session = Session.objects.filter(pc=workstation).order_by('start').values().last()
            latest_sessions[workstation.name] = latest_session

        response = {
            "rooms": rooms,
            "workstations": latest_sessions
        }

        return Response(response, HTTP_200_OK)

class StartSession(APIView):
    def post(self, request):
        pc = request.data.get('pc')
        timestamp = request.data.get('timestamp')      

        if pc is None or timestamp is None:
            return Response({'error': 'Debe ingresar pc y timestamp'},
                        status=HTTP_400_BAD_REQUEST)
        try:
            ws = Workstation.objects.get(name=pc)
        except Workstation.DoesNotExist:
            return Response({'error': 'No existe el PC'},
                        status=HTTP_404_NOT_FOUND)
        
        Session.objects.create(pc=ws, start=timestamp)
        
        return Response(status=HTTP_200_OK)
    
class EndSession(APIView):
    def post(self, request):
        pc = request.data.get('pc')
        start = request.data.get('start') 
        timestamp = request.data.get('timestamp')      

        if pc is None or start is None or timestamp is None:
            return Response({'error': 'Debe ingresar pc, start timestamp y end timestamp.'},
                        status=HTTP_400_BAD_REQUEST)
        
        if start > timestamp:
            return Response({'error': 'El cierre de sesión no puede ocurrir antes del inicio.'},
                        status=HTTP_400_BAD_REQUEST)
        
        try:
            ws = Workstation.objects.get(name=pc)
        except Workstation.DoesNotExist:
            return Response({'error': 'No existe el PC'},
                        status=HTTP_404_NOT_FOUND)
        
        try:
            current = Session.objects.get(pc=ws, start=start)
        except Session.DoesNotExist:
            return Response({'error': 'No hay registro de un inicio del pc en el tiempo dado.'},
                        status=HTTP_404_NOT_FOUND)
        
        current.end = timestamp
        current.save()
        
        return Response(status=HTTP_200_OK)
    
class Alive(APIView):
    def post(self, request):
        pc = request.data.get('pc')
        start = request.data.get('start')
        timestamp = request.data.get('timestamp')

        if pc is None or start is None or timestamp is None:
            return Response({'error': 'Debe ingresar pc, start timestamp y end timestamp.'},
                        status=HTTP_400_BAD_REQUEST)
        
        try:
            ws = Workstation.objects.get(name=pc)
        except Workstation.DoesNotExist:
            return Response({'error': 'No existe el PC'},
                        status=HTTP_404_NOT_FOUND)
        
        try:
            current = Session.objects.get(pc=ws, start=start)
        except Session.DoesNotExist:
            return Response({'error': 'No hay registro de un inicio del pc en el tiempo dado.'},
                        status=HTTP_404_NOT_FOUND)
        
        current.alive = timestamp
        current.save()
        return Response(status=HTTP_200_OK)
    

def getHourlyGranularity(start, end):
    step = 3600000
    ranges = []
    i = start    
    while (i + step < end):
        ranges.append((i, i + step))
        i += step
    ranges.append((i, end))
    return ranges

def getDailyGranularity(start, end):
    step = 86400000
    eod = getEndOfDay(start) + 1
    ranges = [(start, eod)]
    i = eod
    while i + step < end:
        ranges.append((i, i + step))
        i += step
    ranges.append((i, end))
    return ranges


def getEndOfDay(timestamp):
    dt = datetime.fromtimestamp(timestamp / 1000)
    endOfDay = time(23, 59, 59, 999999)
    endDt = datetime.combine(dt.date(), endOfDay)
    endTimestamp = int(endDt.timestamp() * 1000)
    return endTimestamp

def getStartOfDay(timestamp):
    dt = datetime.fromtimestamp(timestamp / 1000)
    startOfDay = time(0, 0, 0, 0)
    startDt = datetime.combine(dt.date(), startOfDay)
    startTimestamp = int(startDt.timestamp() * 1000)
    return startTimestamp