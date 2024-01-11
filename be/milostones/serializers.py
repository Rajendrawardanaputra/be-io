# serializers.py
from rest_framework import serializers
from .models import Milostones, ProjectCharter, User, ActivityLog
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

class MilostonesSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    status_milostones = serializers.CharField(read_only=True)

    class Meta:
        model = Milostones
        fields = '__all__'

    def validate(self, data):
        milestone = data.get('milestone', '')
        deskripsi = data.get('deskripsi', '')
        tanggal = data.get('tanggal', '')
        id_charter = data.get('id_charter')
        id_user = data.get('id_user')

        if milestone and deskripsi and tanggal and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_milostones ke 'done'
            data['status_milostones'] = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_milostones ke 'draft'
            data['status_milostones'] = 'draft'

        return data
    
    def create(self, validated_data):
        milostones = super().create(validated_data)
        self.log_activity(milostones.id_user.pk, 'created', 'Milostones', milostones)
        return milostones
    
    def update(self, instance, validated_data):
        # Update objek dengan nilai-nilai baru
        for key, value in validated_data.items():
            setattr(instance, key, value)

        milestone = instance.milestone
        deskripsi = instance.deskripsi
        tanggal = instance.tanggal
        id_charter = instance.id_charter
        id_user = instance.id_user_id

        if milestone and deskripsi and tanggal and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_milostones ke 'done'
            instance.status_milostones = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_milostones ke 'draft'
            instance.status_milostones = 'draft'

        instance.save()
        self.log_activity(instance.id_user.pk, 'updated', 'Milostones', instance)
        return instance
    
    def log_activity(self, user_id, action, name_table, milostones):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'tanggal': milostones.tanggal,
            'milestone': milostones.milestone,
            'deskripsi': milostones.deskripsi,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class MilostonesListSerializer(serializers.ListSerializer):
    child = MilostonesSerializer()
