from django.contrib import admin
from .models import Report,Revision, ScheduledReview,Externuser


admin.site.register(Report)
admin.site.register(Revision)
admin.site.register(ScheduledReview)
admin.site.register(Externuser)
