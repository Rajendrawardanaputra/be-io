from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import ProjectInternal
from rest_framework import serializers
from rest_framework import status
from .serializers import ProjectInternalSerializer
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
#from be.middleware.token_middleware import CustomJWTAuthentication
from jwt import ExpiredSignatureError, InvalidTokenError
from django.http import JsonResponse
from datetime import datetime
import boto3
from django.conf import settings
import json
from urllib.parse import quote
import botocore
import os
from be.middleware.token_middleware import CustomJWTAuthentication
from jwt import ExpiredSignatureError, InvalidTokenError



class ProjectInternalListCreateView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]

    queryset = ProjectInternal.objects.all()
    serializer_class = ProjectInternalSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('id_project')
        serializer = self.get_serializer(queryset, many=True)
        response_data = self.get_response_data(queryset, serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        queryset = self.get_queryset()
        response_data = self.get_response_data(queryset, serializer.data)

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_response_data(self, queryset, serialized_data):
        total_projects = queryset.count()
        total_ON_GOING = queryset.filter(status='ON_GOING').count()
        total_DROPPED = queryset.filter(status='DROPPED').count()
        total_FINISH = queryset.filter(status='FINISH').count()

        return {
            'total_projects': total_projects,
            'total_ON_GOING': total_ON_GOING,
            'total_DROPPED': total_DROPPED,
            'total_FINISH': total_FINISH,
            'projects': serialized_data,
        }
    
    def perform_create(self, serializer):
     validated_data = serializer.validated_data
     photo_hld = validated_data['hld']
     photo_lld = validated_data['lld']

     current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

     s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    
    # Proses untuk foto hld
     photo_hld_name = f"hld/{current_datetime}_{photo_hld.name}"
     photo_hld_url = f"/internalorder/{photo_hld_name}"

    # Proses untuk foto lld
     photo_lld_name = f"lld/{current_datetime}_{photo_lld.name}"
     photo_lld_url = f"/internalorder/{photo_lld_name}"

     serializer.save(hld=photo_hld_url, lld=photo_lld_url)

    # Simpan foto hld
     s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        Key=photo_hld_name, Body=photo_hld, ContentType='image/jpeg')     

    # Simpan foto lld
     s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        Key=photo_lld_name, Body=photo_lld, ContentType='image/jpeg')     

     return Response({"message": "Foto HLD dan LLD diunggah", "hld": photo_hld_url, "lld": photo_lld_url}, status=status.HTTP_201_CREATED)



class ProjectInternalRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ProjectInternal.objects.all()
    serializer_class = ProjectInternalSerializer

    def perform_update(self, serializer):
        # Hapus foto profil lama dari S3 saat pembaruan
        old_photo_hld = serializer.instance.hld
        new_photo_hld = self.request.data.get('hld')

        old_photo_lld = serializer.instance.lld
        new_photo_lld = self.request.data.get('lld')
        
        data = {}

        # Inisialisasi photo_hld dan photo_lld dengan nilai yang sesuai
        photo_hld = old_photo_hld
        photo_lld = old_photo_lld

        if new_photo_hld is not None and hasattr(new_photo_hld, 'size'):
            # Validasi ukuran gambar (maksimal 5 MB)
            max_size_bytes = 5 * 1024 * 1024 
            if new_photo_hld.size > max_size_bytes:
                raise serializers.ValidationError("Ukuran gambar tidak boleh melebihi 5 MB.")

            # Validasi tipe gambar (opsional)
            valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/jfif']
            if new_photo_hld.content_type not in valid_image_types:
                raise serializers.ValidationError("Tipe gambar tidak valid. Harap unggah gambar JPEG, PNG, atau GIF.")

            s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            new_photo_profile_name = f"hld/{current_datetime}_{new_photo_hld.name}"
            photo_hld = f"/internalorder/{new_photo_profile_name}"

            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=new_photo_profile_name, Body=new_photo_hld, ContentType='image/jpeg')
            
            if old_photo_hld:
                old_photo_profile_name = old_photo_hld.name.split('/')[-1]
                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).delete_objects(Delete={'Objects': [{'Key': f'hld/{old_photo_profile_name}'}]})
            
            data["hld"] = photo_hld  # Tambahkan data hld ke dictionary
        elif new_photo_hld is None:
            # Jika tidak ada file hld yang disertakan dalam pembaruan,
            # pertahankan nilai yang ada pada objek sebelumnya
            data["hld"] = old_photo_hld

        if new_photo_lld is not None and hasattr(new_photo_lld, 'size'):
            # Validasi ukuran gambar (maksimal 5 MB)
            max_size_bytes = 5 * 1024 * 1024 
            if new_photo_lld.size > max_size_bytes:
                raise serializers.ValidationError("Ukuran gambar tidak boleh melebihi 5 MB.")

            # Validasi tipe gambar (opsional)
            valid_image_types = ['image/jpeg', 'image/png', 'image/gif', 'image/jfif']
            if new_photo_lld.content_type not in valid_image_types:
                raise serializers.ValidationError("Tipe gambar tidak valid. Harap unggah gambar JPEG, PNG, atau GIF.")

            s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            new_photo_profile_name = f"lld/{current_datetime}_{new_photo_lld.name}"
            photo_lld = f"/internalorder/{new_photo_profile_name}"

            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=new_photo_profile_name, Body=new_photo_lld, ContentType='image/jpeg')

            if old_photo_lld:
                old_photo_profile_name = old_photo_lld.name.split('/')[-1]
                s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).delete_objects(Delete={'Objects': [{'Key': f'lld/{old_photo_profile_name}'}]})
            
            data["lld"] = photo_lld  # Tambahkan data lld ke dictionary
        elif new_photo_lld is None:
            # Jika tidak ada file lld yang disertakan dalam pembaruan,
            # pertahankan nilai yang ada pada objek sebelumnya
            data["lld"] = old_photo_lld

        serializer.save(**data)
        return Response({"message": "Update berhasil"}, status=status.HTTP_200_OK)


    # def perform_update(self, serializer):
    #     validated_data = serializer.validated_data
    #     photo_hld = validated_data.get('hld', None)
    #     photo_lld = validated_data.get('lld', None)

    #     # Inisialisasi sumber daya AWS S3 di luar loop
    #     s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    #     bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    #     # Update foto hld
    #     if photo_hld:
    #         self._handle_old_file(bucket, serializer.instance.hld)
    #         photo_hld_url = self._process_photo_update(photo_hld, "hld")
    #         serializer.save(hld=photo_hld_url)

    #     # Update foto lld
    #     if photo_lld:
    #         self._handle_old_file(bucket, serializer.instance.lld)
    #         photo_lld_url = self._process_photo_update(photo_lld, "lld")
    #         serializer.save(lld=photo_lld_url)

    #     # Lanjutkan dengan pembaruan sisa atribut lainnya jika ada
    #     super().perform_update(serializer)

    #     # Tanggapan JSON yang konsisten
    #     response_data = {
    #         "message": "Foto HLD dan LLD diupdate",
    #         "hld": photo_hld_url if photo_hld else None,
    #         "lld": photo_lld_url if photo_lld else None
    #     }
    #     return Response(response_data, status=status.HTTP_200_OK)

    # def _handle_old_file(self, bucket, old_url):
    #     if old_url:
    #         old_key = os.path.basename(str(old_url))
    #         try:
    #             obj = bucket.Object(old_key)
    #             obj.load()
    #             bucket.delete_objects(Delete={'Objects': [{'Key': old_key}]})
    #         except botocore.exceptions.ClientError as e:
    #             if e.response['Error']['Code'] == '404':
    #                 pass  # Objek tidak ditemukan, tidak perlu dihapus
    #             else:
    #                 raise  # Kesalahan lain

    # def _process_photo_update(self, photo, folder):
    #     current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    #     photo_name = f"{folder}/{current_datetime}_{os.path.basename(photo.name)}"
    #     photo_url = f"/internalorder/{quote(photo_name)}"
        
    #     s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
    #         Key=photo_name, Body=photo.read(), ContentType='image/jpeg')
        
    #     return photo_url
            