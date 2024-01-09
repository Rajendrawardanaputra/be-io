from rest_framework import serializers
from .models import ProjectInternal, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectInternalSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True)  # Tambahkan source='id_user' di sini
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

    def get_total_weeks(self, instance):
        start_date = instance.start_date
        end_date = instance.end_date

        # Hitung selisih waktu antara start_date dan end_date
        delta = end_date - start_date

        # Hitung jumlah minggu, dengan asumsi 4 minggu per bulan
        total_weeks = (delta.days // 7) + (delta.days % 30 >= 7)

        return total_weeks
