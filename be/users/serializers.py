from django.core.exceptions import ValidationError
from django.db.models import Q
import bcrypt
from rest_framework import serializers
from .models import User
from urllib.parse import urlparse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'hak_akses', 'nama', 'email', 'phone', 'jabatan', 'profile', 'password']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Modifikasi URL struktur_organisasi sesuai kebutuhan Anda
        if representation['profile']:
            url_parts = urlparse(representation['profile'])
            representation['profile'] = url_parts.path

        return representation

    def validate_email(self, value):
        user_id = self.instance.id_user if self.instance else None
        existing_user = User.objects.filter(Q(email=value) & ~Q(id_user=user_id)).first()

        if existing_user:
            raise serializers.ValidationError("Email sudah terdaftar. Gunakan email lain.")

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Mendapatkan 'password' dari data yang divalidasi
        password = validated_data.pop('password', None)

        # Memperbarui instance dengan data yang divalidasi
        instance = super().update(instance, validated_data)

        # Jika 'password' disertakan, update password
        if password is not None:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            instance.password = hashed_password.decode('utf-8')

        instance.save()
        return instance
