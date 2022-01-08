from django.contrib import admin
from .models import TicketReport,Revision, ScheduledReview,Externuser


admin.site.register(TicketReport)
admin.site.register(Revision)
admin.site.register(ScheduledReview)
admin.site.register(Externuser)
