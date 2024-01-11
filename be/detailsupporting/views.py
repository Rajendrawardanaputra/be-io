from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import RoleResponsibilities, User, ActivityLog
from .serializers import RoleResponsibilitiesSerializer
import boto3
from datetime import datetime
from django.conf import settings
from rest_framework import serializers
from be.middleware.token_middleware import CustomJWTAuthentication
from django.shortcuts import get_object_or_404
import json

class RoleResponsibilitiesListView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = RoleResponsibilities.objects.all()
    serializer_class = RoleResponsibilitiesSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        photo_struktur_organisasi = validated_data.get('struktur_organisasi')

        if photo_struktur_organisasi:
            max_size_bytes = 5 * 1024 * 1024 
            if photo_struktur_organisasi.size > max_size_bytes:
                raise serializers.ValidationError({"error": "Maximum size for profile photo is 5MB"})

            valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/jfif']
            if photo_struktur_organisasi.content_type not in valid_image_types:
                raise serializers.ValidationError({"error": "Invalid image type. Please upload a JPEG, PNG, JFIF, or GIF image."})

            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

            s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            photo_struktur_organisasi_name = f"struktur_organisasi/{current_datetime}_{photo_struktur_organisasi.name}"
            photo_struktur_organisasi_url = f"/internalorder/{photo_struktur_organisasi_name}"

            serializer.save(struktur_organisasi=photo_struktur_organisasi_url, status_responsibilities='done')

            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=photo_struktur_organisasi_name, Body=photo_struktur_organisasi.read(), ContentType='image/jpeg')

            self.log_activity(serializer.validated_data.get('id_user').id_user, 'created', serializer.instance)

            return Response({"message": "Foto profil diunggah", "image": photo_struktur_organisasi_url}, status=status.HTTP_201_CREATED)
        else:
            serializer.save(status_responsibilities='draft')

            return Response({"message": "Objek Description dibuat tanpa file hlr"}, status=status.HTTP_201_CREATED)
    
    def log_activity(self, user_id, action, roleresponbilites):
         user_instance = get_object_or_404(User, id_user=user_id)
         object_data = {
            'struktur_organisasi_url': roleresponbilites.struktur_organisasi.url if roleresponbilites.struktur_organisasi else None,
        }

         ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table='roleresponbilities',
            object=json.dumps(object_data),
        )
         
class RoleResponsibilitiesDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = RoleResponsibilities.objects.all()
    serializer_class = RoleResponsibilitiesSerializer

    def perform_update(self, serializer):
        old_photo_struktur_organisasi = serializer.instance.struktur_organisasi
        new_photo_struktur_organisasi = self.request.data.get('struktur_organisasi')
        data = {}

        if new_photo_struktur_organisasi:
            # Validasi ukuran gambar (maksimal 5 MB)
            max_size_bytes = 5 * 1024 * 1024
            if new_photo_struktur_organisasi.size > max_size_bytes:
                raise serializers.ValidationError("Ukuran gambar tidak boleh melebihi 5 MB.")

            # Validasi tipe gambar
            valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/jfif']
            if new_photo_struktur_organisasi.content_type not in valid_image_types:
                raise serializers.ValidationError("Tipe gambar tidak valid. Harap unggah gambar JPEG, PNG, atau GIF.")

            s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            new_photo_profile_name = f"struktur_organisasi/{current_datetime}_{new_photo_struktur_organisasi.name}"
            photo_struktur_organisasi = f"/internalorder/{new_photo_profile_name}"

            # Simpan foto baru ke S3
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=new_photo_profile_name, Body=new_photo_struktur_organisasi.read(), ContentType='image/jpeg')

            # Hapus foto lama dari S3
            if old_photo_struktur_organisasi:
                old_photo_profile_name = old_photo_struktur_organisasi.name.split('/')[-1]
                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).delete_objects(Delete={'Objects': [{'Key': f'struktur_organisasi/{old_photo_profile_name}'}]})

            data["struktur_organisasi"] = photo_struktur_organisasi  # Tambahkan data hlr ke dictionary
            data["status_responsibilities"] = "done"  # Perbarui status menjadi 'done'
        elif new_photo_struktur_organisasi is None and old_photo_struktur_organisasi:
            # Jika tidak ada file hlr yang disertakan dalam pembaruan,
            # tetapkan nilai yang ada pada objek sebelumnya
            data["struktur_organisasi"] = old_photo_struktur_organisasi
            data["status_responsibilities"] = "draft"  # Tetapkan status menjadi 'draft'


        serializer.save(**data)

        self.log_activity(serializer.instance.id_user.pk, 'updated', serializer.instance)



    def perform_destroy(self, instance):
        self.log_activity(instance.id_user.pk, 'deleted', instance)
        instance.delete()

    def log_activity(self, user_id, action, roleresponsibilities):
        user_instance = get_object_or_404(User, id_user=user_id)
        object_data = {
            'struktur_organisasi_url': roleresponsibilities.struktur_organisasi.url if roleresponsibilities.struktur_organisasi else None,
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table='roleresponbilities',
            object=json.dumps(object_data),
        )