from rest_framework import serializers
from .models import ProjectInternal, User, ActivityLog
import json
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'nama']

class ProjectInternalSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True)
    total_weeks = serializers.SerializerMethodField()

    class Meta:
        model = ProjectInternal
        fields = ['id_user', 'user', 'id_project', 'status', 'requester', 'application_name', 'start_date', 'end_date', 'total_weeks', 'hld', 'lld', 'brd', 'sequence_number']
        read_only_fields = ['sequence_number']
        ordering = ['id_project']

        extra_kwargs = {
            'start_date': {'required': False},
            'end_date': {'required': False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modifikasi URL struktur_organisasi sesuai kebutuhan Anda
        if representation['hld']:
            url_parts = urlparse(representation['hld'])
            representation['hld'] = url_parts.path
        if representation['lld']:
            url_parts = urlparse(representation['lld'])
            representation['lld'] = url_parts.path

        return representation
    
    def get_total_weeks(self, instance):
        start_date = instance.start_date
        end_date = instance.end_date

        if start_date and end_date:
            delta = end_date - start_date
            total_weeks = (delta.days // 7) + (delta.days % 30 >= 7)
            return total_weeks
        else:
            return None

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Pastikan end_date tidak kurang dari start_date
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("Tanggal selesai tidak boleh sebelum tanggal mulai.")

        return data

    def create(self, validated_data):
        user_id = validated_data['id_user'].pk
        project = super().create(validated_data)

        # Insert activity log for 'created' action
        self.log_activity(user_id, 'created', project)

        return project
        
    def update(self, instance, validated_data):
        user = validated_data.get('id_user', instance.id_user)
        project = super().update(instance, validated_data)

        # Cek perubahan dan log activity
        changed_fields = {}
        for field, value in validated_data.items():
            if getattr(instance, field) != value:
                changed_fields[field] = {
                    'old': getattr(instance, field),
                    'new': value
                }

        self.log_activity(user, 'updated', changed_fields)
        return project

    def log_activity(self, user, action, changed_fields=None):
        if self.instance:
            object_data = {
                'id_project': self.instance.id_project,
                'status': self.instance.status,
                'requester': self.instance.requester,
                'application_name': self.instance.application_name,
                'start_date': str(self.instance.start_date),
                'end_date': str(self.instance.end_date),
                'hld': str(self.instance.hld),
                'lld': str(self.instance.lld),
                'brd': self.instance.brd,
                'sequence_number': self.instance.sequence_number,
            }

            if changed_fields:
                object_data['changed_fields'] = changed_fields

            ActivityLog.objects.create(
                id_user=user,
                action=action,
                name_table='ProjectInternal',
                object=json.dumps(object_data),
            )

