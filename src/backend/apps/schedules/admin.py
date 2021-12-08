from django.contrib import admin
from apps.schedules.models import LabPetition, modulepetition, Module, Event, ModuleEvent

admin.site.register(LabPetition)
admin.site.register(modulepetition)
admin.site.register(Module)
admin.site.register(Event)
admin.site.register(ModuleEvent)

