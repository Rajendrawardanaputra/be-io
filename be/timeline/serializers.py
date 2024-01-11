from rest_framework import serializers
from .models import DetailTimeline, ProjectInternal, User, ActivityLog
import json
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInternal
        fields = ['application_name']

class DetailTimelineSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True)
    project_internal = ProjectInternalSerializer(source='id_project', read_only=True)

    class Meta:
        model = DetailTimeline
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, list):
            return [super(DetailTimelineSerializer, self).to_internal_value(item) for item in data]
        return super(DetailTimelineSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        detail_timeline = super().create(validated_data)
        self.log_activity(detail_timeline.id_user.pk, 'created', 'DetailTimeline', detail_timeline)
        return detail_timeline

    def update(self, instance, validated_data):
        old_activity = instance.activity
        new_activity = validated_data.get('activity', old_activity)

        # Hanya log jika nilai 'activity' berubah
        if old_activity != new_activity:
            self.log_activity(instance.id_user.pk, 'updated', 'activity', old_activity, new_activity)

        return super().update(instance, validated_data)

    def log_activity(self, user_id, action, field_name, old_value=None, new_value=None):
        user_instance = get_object_or_404(User, id_user=user_id)
        instance = getattr(self, 'instance', None)

        if instance is None:
            return  # Tidak ada instance, tidak ada yang bisa dilakukan

        object_data = {
            'weeks': instance.weeks,
            'activity': instance.activity,
            # ... (kolom lainnya)
        }

        # Hanya log jika nilai 'activity' berubah
        if old_value is not None and new_value is not None and old_value != new_value:
            object_data[field_name] = {
                'old_value': old_value,
                'new_value': new_value,
            }

        if field_name == 'id_detail_timeline':
            object_data['id_detail_timeline'] = instance.id_detail_timeline

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table='DetailTimeline',
            object=json.dumps(object_data),
        )

class DetailTimelineListSerializer(serializers.ListSerializer):
    child = DetailTimelineSerializer()
