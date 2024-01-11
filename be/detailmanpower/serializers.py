# serializers.py

from rest_framework import serializers
from .models import DetailMainPower, User, ProjectInternal, ActivityLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInternal
        fields = ['application_name']

class DetailMainPowerSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True)
    project_internal = ProjectInternalSerializer(source='id_project', read_only=True)
    total_man_rate = serializers.ReadOnlyField()

    class Meta:
        model = DetailMainPower
        fields = '__all__'

    def calculate_total_man_rate(self, validated_data):
        man_days_rate = validated_data.get('man_days_rate', 0)
        man_power = validated_data.get('man_power', 0)
        days = validated_data.get('days', 0)
        return man_days_rate * man_power * days

    def create(self, validated_data):
        total_man_rate = self.calculate_total_man_rate(validated_data)
        validated_data['total_man_rate'] = total_man_rate
        detail_main_power = super().create(validated_data)

        # Membuat log aktivitas untuk pembuatan objek
        ActivityLog.objects.create(
            id_user=detail_main_power.id_user,
            action='create',
            name_table='DetailMainPower',
            object=str(detail_main_power),
            name_column='total_man_rate',
            changes=str(total_man_rate)
        )

        return detail_main_power

    def update(self, instance, validated_data):
        total_man_rate = self.calculate_total_man_rate(validated_data)
        instance.man_days_rate = validated_data.get('man_days_rate', instance.man_days_rate)
        instance.man_power = validated_data.get('man_power', instance.man_power)
        instance.days = validated_data.get('days', instance.days)
        instance.total_man_rate = total_man_rate
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        # Membuat log aktivitas untuk pembaruan objek
        ActivityLog.objects.create(
            id_user=instance.id_user,
            action='update',
            name_table='DetailMainPower',
            object=str(instance),
            name_column='total_man_rate',
            changes=str(total_man_rate)
        )

        return instance

class DetailMainPowerListSerializer(serializers.ListSerializer):
    child = DetailMainPowerSerializer()

    def create(self, validated_data):
        return [DetailMainPowerSerializer(data=item).create(item) for item in validated_data]
