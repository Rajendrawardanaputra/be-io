# serializers.py
from rest_framework import serializers
from .models import Status, ProjectCharter, Description, SupportingDoc, Responsibility, Milostones, RoleResponsibilities, DetailResponsibilities

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = '__all__'

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'

class SupportingDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportingDoc
        fields = '__all__'

class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = '__all__'

class MilostonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milostones
        fields = '__all__'

class RoleResponsibilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleResponsibilities
        fields = '__all__'

class DetailResponsibilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailResponsibilities
        fields = '__all__'
