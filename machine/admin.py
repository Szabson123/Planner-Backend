from django.contrib import admin
from .models import *

admin.site.register(Machine)
admin.site.register(Review)
admin.site.register(MachineCommonIssues)
admin.site.register(MachineRareIssues)
admin.site.register(MachineKnowHow)
