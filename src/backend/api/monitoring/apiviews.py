from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.db.models import Q
from apps.monitoring import utils


class GetTickets(APIView):
    """
    title:
    Api monitoreo
    
    description:
    dfasfafsd
    
    get:
    Return count of tickets.

    """
    def get(self, request, format='json'):
        print(utils.count_active_tickets())
        