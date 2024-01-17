# serializers.py
from rest_framework import serializers
from .models import RoleResponsibilities, ProjectCharter, User, ActivityLog
import json
from urllib.parse import urlparse

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modifikasi URL struktur_organisasi sesuai kebutuhan Anda
        if representation['struktur_organisasi']:
            url_parts = urlparse(representation['struktur_organisasi'])
            representation['struktur_organisasi'] = url_parts.path

        return representation


    def validate(self, data):
        struktur_organisasi = data.get('struktur_organisasi', '')
        id_charter = data.get('id_charter')
        id_user = data.get('id_user')

        if struktur_organisasi and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            data['status_responsibilities'] = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            data['status_responsibilities'] = 'draft'

        return data
    
    def create(self, validated_data):
        roleresponsibilities = super().create(validated_data)

        struktur_organisasi = roleresponsibilities.struktur_organisasi
        id_charter = roleresponsibilities.id_charter
        id_user = roleresponsibilities.id_user_id

        if struktur_organisasi  and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            roleresponsibilities.status_responsibilities = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            roleresponsibilities.status_responsibilities = 'draft'

        roleresponsibilities.save()
        self.log_activity(roleresponsibilities.id_user.pk, 'created', 'Roleresponsibilities', roleresponsibilities)
        return roleresponsibilities
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        struktur_organisasi = instance.struktur_organisasi
        id_charter = instance.id_charter
        id_user = instance.id_user_id

        if struktur_organisasi and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            instance.status_responsibilities = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            instance.status_responsibilities = 'draft'

        instance.save()
        self.log_activity(instance.id_user.id_user, 'updated', 'Roleresponbilities', instance)
        return instance
    
    def log_activity(self, user_id, action, name_table, roleresponsibilities):
        object_data = {
            'struktur_organisasi_url': roleresponsibilities.struktur_organisasi.url if roleresponsibilities.struktur_organisasi else None, # Convert date to string 
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user_id=user_id,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

    def delete(self, instance):
        user_id = instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'roleresponbilites', instance)
        instance.delete()
