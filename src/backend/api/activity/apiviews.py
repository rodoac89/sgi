from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from rest_framework.response import Response
from apps.activity.models import Session
from apps.core.models import Workstation
from apps.activity.utils import getSessionsBetweenTimestamps, getSessionsByOption, sessionsToJson, formatSessions

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