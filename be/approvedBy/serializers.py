# serializers.py
from rest_framework import serializers
from .models import Approvedby, ProjectCharter, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class ApprovedbySerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    status_approvedby = serializers.CharField(read_only=True)

    class Meta:
        model = Approvedby
        fields = '__all__'

    def create(self, validated_data):
        # Cek apakah semua bidang telah diisi
        if all(validated_data.values()):
            validated_data['status_approvedby'] = 'done'
        else:
            validated_data['status_approvedby'] = 'draft'

        return super().create(validated_data)
