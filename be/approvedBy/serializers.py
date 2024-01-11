# serializers.py
from rest_framework import serializers
from .models import Approvedby, ProjectCharter, User, ActivityLog
from django.shortcuts import get_object_or_404
import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class ApprovedbySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    project_charter = ProjectCharterSerializer(read_only=True)
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

        approvedby = super().create(validated_data)
        self.log_activity(approvedby.id_user.pk, 'created', 'approvedBy', approvedby)
        return approvedby

    def update(self, instance, validated_data):
        # Update objek dengan nilai-nilai baru
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Cek apakah semua bidang telah diisi
        if all(validated_data.values()):
            instance.status_approvedby = 'done'
        else:
            instance.status_approvedby = 'draft'

        instance.save()
        self.log_activity(instance.id_user.pk, 'updated', 'approvedBy', instance)
        return instance

    def delete(self, instance):
        # Logging activity for each approvedby deletion
        self.log_activity(instance.id_user.pk, 'deleted', 'approvedBy', instance)

        instance.delete()

    def log_activity(self, user_id, action, name_table, approvedby):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'nama': approvedby.nama,
            'cc_to': approvedby.cc_to,
            'note': approvedby.note,
            'title': approvedby.title,
            'nama1': approvedby.nama1,
            'title1': approvedby.title1,
            'cc_to1': approvedby.cc_to1,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )
