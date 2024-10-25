from django.contrib import admin
from .models import Shift, Event, GeneratedPlanner, FreeDay, Availability, ShiftBackup, WeekendEvent, HolyDay


admin.site.register(Shift)
admin.site.register(Event)
admin.site.register(GeneratedPlanner)
admin.site.register(FreeDay)
admin.site.register(Availability)
admin.site.register(ShiftBackup)
admin.site.register(WeekendEvent)
admin.site.register(HolyDay)