from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from apps.authentication import util

class Login(APIView):
    def post(self, request, format='json'):
        username = request.data['username']
        password = request.data['password']
        if username is None and password is None:
            return Response({'error': 'Debe ingresar nombre de usuario y contraseña'},
                        status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username,password=password)
        if not user:
            return Response({'error': 'Credenciales incorrectas'},
                        status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)

        response = util.auth_profile(token, user)
        
        return Response(response,
                        status=HTTP_200_OK)

class Logout(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response({'detail':'Sesión cerrada con exito'},status=HTTP_200_OK)