from django.contrib import admin
from .models import Shift, Event, GeneratedPlanner, FreeDay, Availability


admin.site.register(Shift)
admin.site.register(Event)
admin.site.register(GeneratedPlanner)
admin.site.register(FreeDay)
admin.site.register(Availability)