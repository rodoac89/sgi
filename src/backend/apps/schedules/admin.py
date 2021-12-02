from django.contrib import admin
from apps.schedules.models import LabPetition, modulepetition, module

admin.site.register(LabPetition)
admin.site.register(modulepetition)
admin.site.register(module)
#admin.site.register(Event)
#admin.site.register(Schedule)

