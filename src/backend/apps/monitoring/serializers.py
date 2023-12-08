from rest_framework import serializers
from apps.monitoring.models import TicketReport

class TicketReportSerializer(serializers.Serializer):
    
    class Meta:
        model = TicketReport
        fields = '__all__'
    
    @classmethod
    def get_count(self, obj):
        return obj.count()

