from rest_framework import serializers
from .models import DetailTimeline, ProjectInternal, User

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
        fields = '__all__'  # Tambahkan 'project_internal' ke dalam fields

    def to_internal_value(self, data):
        if isinstance(data, list):
            return [super(DetailTimelineSerializer, self).to_internal_value(item) for item in data]
        return super(DetailTimelineSerializer, self).to_internal_value(data)

class DetailTimelineListSerializer(serializers.ListSerializer):
    child = DetailTimelineSerializer()

