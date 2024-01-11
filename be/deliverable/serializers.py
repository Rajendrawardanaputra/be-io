# serializers.py
from rest_framework import serializers
from .models import Deliverable, ProjectCharter, User, ActivityLog
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

class DeliverableSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    
    # Mengatur status_deliverable menjadi read-only
    status_deliverable = serializers.CharField(read_only=True)

    class Meta:
        model = Deliverable
        fields = '__all__'

    def validate(self, data):
        deliverables = data.get('deliverables', [])
        if deliverables:
            # Jika deliverables diisi, atur status_deliverable ke 'done'
            data['status_deliverable'] = 'done'
        else:
            # Jika deliverables kosong, atur status_deliverable ke 'draft'
            data['status_deliverable'] = 'draft'

        return data
    
    def create(self, validated_data):
        deliverable = super().create(validated_data)
        self.log_activity(deliverable.id_user.pk, 'created', 'Deliverables', deliverable)
        return deliverable
    
    def update(self, instance, validated_data):
        # Update objek dengan nilai-nilai baru
        for key, value in validated_data.items():
            setattr(instance, key, value)

        deliverables = instance.deliverables
        id_charter = instance.id_charter
        id_user = instance.id_user_id

        if deliverables and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_deliverable ke 'done'
            instance.status_deliverable = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_deliverable ke 'draft'
            instance.status_deliverable = 'draft'

        instance.save()
        self.log_activity(instance.id_user.pk, 'updated', 'Deliverables', instance)
        return instance
    
    def log_activity(self, user_id, action, name_table, deliverable):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'deliverables': deliverable.deliverables,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

    def delete(self, instance):
        # Logging activity for deleted deliverable
        user_id = instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'Deliverables', instance)

        instance.delete()

class DeliverableListSerializer(serializers.ListSerializer):
    child = DeliverableSerializer()
