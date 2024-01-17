from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Description, ActivityLog, User
from .serializers import DescriptionSerializer
from rest_framework.response import Response
from rest_framework import status
from be.middleware.token_middleware import CustomJWTAuthentication
from django.shortcuts import get_object_or_404
import json
import boto3
from datetime import datetime
from django.conf import settings
from rest_framework import serializers

class DescriptionListView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        queryset = Description.objects.all()
        id_charter = self.request.query_params.get('id_charter', None)
        if id_charter:
            queryset = queryset.filter(id_charter=id_charter)
        return queryset

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        file_upload = validated_data.get('hlr')

        if file_upload:
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

            s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            file_name = f"hlr/{current_datetime}_{file_upload.name}"
            file_url = f"/internalorder/{file_name}"

            # Cek apakah ada kolom lain yang kosong atau None, kecuali status_description dan hlr
            if any(value in [None, ""] for key, value in validated_data.items() if key not in ['status_description', 'hlr']):
                serializer.validated_data['status_description'] = 'draft'
            else:
                serializer.validated_data['status_description'] = 'done'

            serializer.save(hlr=file_url)

            # Simpan file ke S3
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=file_name, Body=file_upload, ContentType=file_upload.content_type)

            return Response({"message": "File diunggah", "file_url": file_url}, status=status.HTTP_201_CREATED)
        else:
            # Jika tidak ada file yang diunggah, periksa kolom lainnya
            if any(value in [None, ""] for key, value in validated_data.items() if key != 'status_description'):
                serializer.validated_data['status_description'] = 'draft'
            else:
                serializer.validated_data['status_description'] = 'done'

            serializer.save()

            return Response({"message": "Objek dibuat tanpa file"}, status=status.HTTP_201_CREATED)

    def log_activity(self, user_id, action, name_table, description):
        user_instance = get_object_or_404(User, id_user=user_id)
        object_data = {
            'hlr': description.hlr.url if description.hlr else None,  # Convert date to string
            'assumptions': description.assumptions,
            'contraints': description.contraints,
            'risk': description.risk,
            'key_stakeholders': description.key_stakeholders,
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class DescriptionDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

    def perform_update(self, serializer):
        old_file_hlr = serializer.instance.hlr
        new_file_hlr = self.request.data.get('hlr')
        data = {}

        if new_file_hlr is not None and hasattr(new_file_hlr, 'size'):
            s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            new_file_name = f"hlr/{current_datetime}_{new_file_hlr.name}"
            file_hlr = f"/internalorder/{new_file_name}"

            # Simpan file baru ke S3
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=new_file_name, Body=new_file_hlr, ContentType=new_file_hlr.content_type)

            # Hapus file lama dari S3
            if old_file_hlr:
                # Dapatkan nama file dari atribut name
                old_file_name = old_file_hlr.name.split('/')[-1]
                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).delete_objects(
                    Delete={'Objects': [{'Key': f'hlr/{old_file_name}'}]})

            data["hlr"] = file_hlr  # Tambahkan data hlr ke dictionary
        elif new_file_hlr is None and old_file_hlr:
            # Jika tidak ada file hlr yang disertakan dalam pembaruan,
            # tetapkan nilai yang ada pada objek sebelumnya
            data["hlr"] = old_file_hlr.url  # Menggunakan url untuk file_hlr
        else:
            # Jika tidak ada perubahan pada field 'hlr'
            data["hlr"] = serializer.instance.hlr.url if serializer.instance.hlr else None  # Menggunakan url untuk file_hlr

        # Cek apakah ada kolom lain yang kosong atau None, kecuali status_description dan hlr
        if any(value in [None, ""] for key, value in serializer.validated_data.items() if key not in ['status_description', 'hlr']):
            serializer.validated_data['status_description'] = 'draft'
        else:
            serializer.validated_data['status_description'] = 'done'

        serializer.save(**data)

        self.log_activity(serializer.instance.id_user.pk, 'updated', 'Description', serializer.instance)

        return Response({"message": "Objek berhasil diperbarui"}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        # Hapus file hlr dari S3 saat objek dihapus
        s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        old_file_hlr = instance.hlr

        if old_file_hlr:
            # Dapatkan nama file dari atribut name
            old_file_name = old_file_hlr.name.split('/')[-1]
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).delete_objects(
                Delete={'Objects': [{'Key': f'hlr/{old_file_name}'}]})

        self.log_activity(instance.id_user.pk, 'deleted', 'Description', instance)

        instance.delete()

        return Response({"message": "Objek berhasil dihapus"}, status=status.HTTP_204_NO_CONTENT)

    def log_activity(self, user_id, action, name_table, description):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'hlr': description.hlr.url if description.hlr else None,
            'assumptions': description.assumptions,
            'contraints': description.contraints,
            'risk': description.risk,
            'key_stakeholders': description.key_stakeholders,
            # ... (Tambahkan kolom lainnya jika diperlukan)
        }   

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )
