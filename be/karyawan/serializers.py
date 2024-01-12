from rest_framework import serializers
from .models import ActivityLog, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['hak_akses', 'nama']
class ActivityLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True)
    class Meta:
        model = ActivityLog
        fields = ['id_activity', 'id_user', 'user', 'action', 'name_table', 'object', 'createdAt', 'updatedAt']
