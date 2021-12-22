from django.contrib import admin
from apps.schedules.models import RoomPetition, Module, Event, ModuleEvent

admin.site.register(RoomPetition)
admin.site.register(Module)
admin.site.register(Event)
admin.site.register(ModuleEvent)

