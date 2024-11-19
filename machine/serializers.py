from rest_framework import serializers

from .models import *
from custom_user.models import CustomUser


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'location', 'description']
        

class ReviewSerializer(serializers.ModelSerializer):
    machine_name = serializers.SerializerMethodField()
    machine_id = serializers.IntegerField(source='machine.id', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'machine_name' ,'date', 'description', 'done', 'machine_id']
        
    def get_machine_name(self, obj):
        return obj.machine.name
    

class MachineRareIssuesSerializer(serializers.ModelSerializer):
    machine_name = serializers.SerializerMethodField()
    
    class Meta:
        model = MachineRareIssues
        fields = ['id', 'name', 'data', 'what_problem', 'how_fix', 'machine_name']
        
    def get_machine_name(self, obj):
        return obj.machine.name
    

class MachineCommonIssuesSerializer(serializers.ModelSerializer):
    machine_name = serializers.SerializerMethodField()
    
    class Meta:
        model = MachineCommonIssues
        fields = ['id', 'name', 'added_data', 'what_problem', 'how_fix', 'machine_name']
        
    def get_machine_name(self, obj):
        return obj.machine.name
    

class MachineKnowHowSerializer(serializers.ModelSerializer):
    machine_name = serializers.SerializerMethodField()
    
    class Meta:
        model = MachineKnowHow
        fields = ['id', 'machine_name', 'name' ,'added_data', 'how_to_do']
    
    def get_machine_name(self, obj):
        return obj.machine.name
    
# READ
class MachineWholeinfoSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(read_only=True, many=True)
    common = MachineCommonIssuesSerializer(read_only=True, many=True)
    knowhow = MachineKnowHowSerializer(read_only=True, many=True)
    rare = MachineRareIssuesSerializer(read_only=True, many=True)
    
    class Meta:
        model = Machine
        fields = ['id', 'name', 'location', 'description', 'review', 'common', 'knowhow', 'rare']