from rest_framework import serializers

from .models import Raport
from custom_user.models import CustomUser


class RaportSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Raport
        fields = ['id', 'date', 'text', 'user', 'user_name']
        
    def get_user_name(self, obj):
        first_name = obj.user.first_name or ''
        last_name = obj.user.last_name or ''
        return f"{first_name} {last_name}".strip()