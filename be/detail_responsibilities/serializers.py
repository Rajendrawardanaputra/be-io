from rest_framework import serializers
from .models import DetailResponsibilities, ProjectCharter, User, ActivityLog
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

class DetailResponsibilitiesSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    status_detailresponsibilities = serializers.CharField(read_only=True)
    
    class Meta:
        model = DetailResponsibilities
        fields = '__all__'

    def validate(self, data):
        nama_pc = data.get('nama_pc', '')
        role_pc = data.get('role_pc', '')
        description = data.get('description', '')
        id_responsibilities = data.get('id_responsibilities')
        id_charter = data.get('id_charter')
        id_user = data.get('id_user')

        if nama_pc and role_pc and description and id_responsibilities is not None and id_charter is not None  and id_user is not None:
            data['status_detailresponsibilities'] = 'done'
        else:
            data['status_detailresponsibilities'] = 'draft'

        return data
    
    def create(self, validated_data):
        detailresponsibilities = super().create(validated_data)
        self.log_activity(detailresponsibilities.id_user.pk, 'created', 'Detailresponbilities', detailresponsibilities)
        return detailresponsibilities
    
    def update(self, instance, validated_data):
        # Update objek dengan nilai-nilai baru
        for key, value in validated_data.items():
            setattr(instance, key, value)

        nama_pc = instance.nama_pc
        role_pc = instance.role_pc
        description = instance.description
        id_responsibilities = instance.id_responsibilities
        id_charter = instance.id_charter
        id_user = instance.id_user_id

        if nama_pc and role_pc and description and id_responsibilities is not None and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_milostones ke 'done'
            instance.status_detailresponsibilities = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_milostones ke 'draft'
            instance.status_detailresponsibilities = 'draft'

        instance.save()
        self.log_activity(instance.id_user.pk, 'updated', 'Detailresponbilities', instance)
        return instance
    
    def log_activity(self, user_id, action, name_table, detailresponsibilities):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'nama_pc': detailresponsibilities.nama_pc,
            'role_pc': detailresponsibilities.role_pc,
            'description': detailresponsibilities.description,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )
     
class DetailResponsibilitiesListSerializer(serializers.ListSerializer):
    child = DetailResponsibilitiesSerializer()
