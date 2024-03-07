from rest_framework import serializers
from .models import SupportingDoc, ProjectCharter, User, ActivityLog
from urllib.parse import urlparse
import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class SupportingDocSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    
    class Meta:
        model = SupportingDoc
        exclude = ['document'] 
        read_only_fields = ['status_supportingdoc']


    def validate(self, data):
        document_name = data.get('document_name', '')
        notes = data.get('notes', '')
        id_charter = data.get('id_charter')
        id_user = data.get('id_user')

        if document_name and notes and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            data['status_supportingdoc'] = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            data['status_supportingdoc'] = 'draft'

        return data
    
    def create(self, validated_data):
        supporting = super().create(validated_data)

        document_name = supporting.document_name
        notes = supporting.notes
        id_charter = supporting.id_charter
        id_user = supporting.id_user_id

        if document_name and notes and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            supporting.status_supportingdoc = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            supporting.status_supportingdoc = 'draft'

        supporting.save()
        self.log_activity(supporting.id_user.pk, 'created', 'SupportingDoc', supporting)
        return supporting
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        document_name = instance.document_name
        notes = instance.notes
        id_charter = instance.id_charter
        id_user = instance.id_user_id

        if document_name and notes and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            instance.status_supportingdoc = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            instance.status_supportingdoc = 'draft'

        instance.save()
        self.log_activity(instance.id_user.id_user, 'updated', 'SupportingDoc', instance)
        return instance
    
    def log_activity(self, user_id, action, name_table, supporting):
        object_data = {
            'document_name': supporting.document_name,
            'notes': supporting.notes,
            'document_url': supporting.document.url if supporting.document else None, # Convert date to string 
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
        self.log_activity(user_id, 'deleted', 'supporting', instance)
        instance.delete()

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportingDoc
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modifikasi URL struktur_organisasi sesuai kebutuhan Anda
        if representation['document']:
            url_parts = urlparse(representation['document'])
            representation['document'] = url_parts.path

        return representation

class SupportingListSerializer(serializers.ListSerializer):
    child = SupportingDocSerializer()

