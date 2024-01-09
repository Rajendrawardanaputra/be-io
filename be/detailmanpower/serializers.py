# serializers.py

from rest_framework import serializers
from .models import DetailMainPower, User, ProjectInternal


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
        # Menghitung dan mengatur total_man_rate saat pembuatan objek
        total_man_rate = self.calculate_total_man_rate(validated_data)
        validated_data['total_man_rate'] = total_man_rate
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Menghitung dan mengatur total_man_rate saat pembaruan objek
        total_man_rate = self.calculate_total_man_rate(validated_data)
        instance.man_days_rate = validated_data.get('man_days_rate', instance.man_days_rate)
        instance.man_power = validated_data.get('man_power', instance.man_power)
        instance.days = validated_data.get('days', instance.days)
        instance.total_man_rate = total_man_rate
        instance.role = validated_data.get('role', instance.role)  # Memperbarui bidang role
        instance.save()
        return instance

class DetailMainPowerListSerializer(serializers.ListSerializer):
    child = DetailMainPowerSerializer()

    def create(self, validated_data):
        return [DetailMainPowerSerializer(data=item).create(item) for item in validated_data]
