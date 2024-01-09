from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Description
from .serializers import DescriptionSerializer
from rest_framework.response import Response
from rest_framework import status
from be.middleware.token_middleware import CustomJWTAuthentication

import boto3
from datetime import datetime
from django.conf import settings
from rest_framework import serializers

class DescriptionListView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]

    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer

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
        
class DescriptionDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    
    queryset = Description.objects.all()
    serializer_class = DescriptionSerializer
    
    def perform_update(self, serializer):
        # Hapus file lama dari S3 saat pembaruan
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
                old_file_name = old_file_hlr.split('/')[-1]
                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).delete_objects(Delete={'Objects': [{'Key': f'hlr/{old_file_name}'}]})

            data["hlr"] = file_hlr  # Tambahkan data hlr ke dictionary
        elif new_file_hlr is None and old_file_hlr is not None:
            # Jika tidak ada file hlr yang disertakan dalam pembaruan,
            # tetapkan nilai yang ada pada objek sebelumnya
            data["hlr"] = old_file_hlr
        else:
            # Jika tidak ada perubahan pada field 'hlr'
            data["hlr"] = serializer.instance.hlr

        # Cek apakah ada kolom lain yang kosong atau None, kecuali status_description dan hlr
        if any(value in [None, ""] for key, value in serializer.validated_data.items() if key not in ['status_description', 'hlr']):
            serializer.validated_data['status_description'] = 'draft'
        else:
            serializer.validated_data['status_description'] = 'done'

        serializer.save(**data)

        return Response({"message": "Objek berhasil diperbarui"}, status=status.HTTP_200_OK)
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(serializer)
        return Response({'message': 'Data deleted successfully'})
    
    def perform_destroy(self, serializer):
        # Hapus foto profil dari S3 ketika pengguna dihapus
        s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        
        old_photo_hlr = serializer.instance.hlr

        if old_photo_hlr:
            # Menggunakan 'name' untuk mendapatkan nama berkas
            old_photo_hlr_name = old_photo_hlr.split('/')[-1]
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).delete_objects(Delete={'Objects': [{'Key': f'hlr/{old_photo_hlr_name}'}]})

        serializer.instance.delete()
