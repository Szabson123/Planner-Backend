from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'is_central')}),
    )
    list_display = UserAdmin.list_display + ('phone_number', 'is_central')

admin.site.register(CustomUser, CustomUserAdmin)