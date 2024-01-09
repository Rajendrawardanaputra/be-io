# serializers.py
from rest_framework import serializers
from .models import RoleResponsibilities, ProjectCharter, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class RoleResponsibilitiesSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    
    class Meta:
        model = RoleResponsibilities
        fields = '__all__'
        read_only_fields = ['status_responsibilities']
