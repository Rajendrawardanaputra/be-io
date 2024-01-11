# serializers.py
from rest_framework import serializers
from .models import Responsibility, ProjectCharter, User, ActivityLog
import json
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class ResponsibilitySerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True)
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)

    class Meta:
        model = Responsibility
        fields = '__all__'
        read_only_fields = ['status_responsibility']

    def validate(self, data):
        pm_responsibility = data.get('pm_responsibility', '')
        project_value = data.get('project_value', '')
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        id_charter = data.get('id_charter')
        id_user = data.get('id_user')

        if pm_responsibility and project_value and start_date and end_date and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_responsibility ke 'done'
            data['status_responsibility'] = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_responsibility ke 'draft'
            data['status_responsibility'] = 'draft'

        return data
    
    def create(self, validated_data):
        responsibility = super().create(validated_data)
        self.log_activity(responsibility.id_user.pk, 'created', 'Responsibility', responsibility)
        return responsibility
    
    def update(self, instance, validated_data):
        # Update objek dengan nilai-nilai baru
        for key, value in validated_data.items():
            setattr(instance, key, value)

        pm_responsibility = instance.pm_responsibility
        project_value = instance.project_value
        start_date = instance.start_date
        end_date = instance.end_date
        id_charter = instance.id_charter
        id_user = instance.id_user_id

        if pm_responsibility and project_value and start_date and end_date and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_responsibility ke 'done'
            instance.status_responsibility = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_responsibility ke 'draft'
            instance.status_responsibility = 'draft'

        instance.save()
        self.log_activity(instance.id_user.pk, 'updated', 'Responsibility', instance)
        return instance
    
    def log_activity(self, user_id, action, name_table, responsibility):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'pm_responsibility': responsibility.pm_responsibility,
            'project_value': responsibility.project_value,
            'start_date': str(responsibility.start_date),  # Convert date to string
            'end_date': str(responsibility.end_date), 
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

    def delete(self, instance):
        # Logging activity for deleted responsibility
        user_id = instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'responsibility', instance)

        instance.delete()
