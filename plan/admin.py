from django.contrib import admin
from .models import Shift, Event, WorkingHours


admin.site.register(Shift)
admin.site.register(Event)
admin.site.register(WorkingHours)