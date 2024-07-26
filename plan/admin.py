from django.contrib import admin
from .models import Shift, Event, GeneratedPlanner


admin.site.register(Shift)
admin.site.register(Event)
admin.site.register(GeneratedPlanner)