from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectInternal, User, ActivityLog
from .serializers import ProjectInternalSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
from django.shortcuts import get_object_or_404
from datetime import datetime
import boto3
import json
from urllib.parse import quote
import os
from django.conf import settings
from rest_framework import serializers

class ProjectInternalListCreateView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = ProjectInternal.objects.all()
    serializer_class = ProjectInternalSerializer

    def get_queryset(self):
        queryset = ProjectInternal.objects.all()
        id_user = self.request.query_params.get('id_user', None)
        
        if id_user:
            queryset = queryset.filter(id_user=id_user)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('id_project')
        serializer = self.get_serializer(queryset, many=True)
        response_data = self.get_response_data(queryset, serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Insert activity log for 'created' action
        self.log_activity(serializer.validated_data['id_user'].pk, 'created', serializer.instance)

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

    def log_activity(self, user_id, action, project):
        user_instance = get_object_or_404(User, id_user=user_id)
    
        if project:
            object_data = {
                'id_project': project.id_project,
                'status': project.status,
                'requester': project.requester,
                'application_name': project.application_name,
                'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
                'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
                'hld': str(project.hld),
                'lld': str(project.lld),
                'brd': project.brd,
                'sequence_number': project.sequence_number,
            }

            ActivityLog.objects.create(
                id_user=user_instance,
                action=action,
                name_table='ProjectInternal',
                object=json.dumps(object_data),
            )
            
            return Response({"message": f"ProjectInternal berhasil di{action}"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "ProjectInternal tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

class ProjectInternalRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = ProjectInternal.objects.all()
    serializer_class = ProjectInternalSerializer

    def get_queryset(self):
        queryset = ProjectInternal.objects.all()
        id_user = self.request.query_params.get('id_user', None)
        
        if id_user:
            queryset = queryset.filter(id_user=id_user)
        
        return queryset 

    def perform_update(self, serializer):
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
            
            data["hld"] = photo_hld
            self.log_activity(serializer.instance.id_user.pk, 'updated', 'hld', old_photo_hld, new_photo_hld)
        elif new_photo_hld is None:
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
            
            data["lld"] = photo_lld
            self.log_activity(serializer.instance.id_user.pk, 'updated', 'lld', old_photo_lld, new_photo_lld)
        elif new_photo_lld is None:
            data["lld"] = old_photo_lld

        serializer.save(**data)
        return Response({"message": "Update berhasil"}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        user_id = instance.id_user.pk
        self.log_activity(user_id, 'deleted', 'ProjectInternal', instance)
        instance.delete()
        return Response({"message": "ProjectInternal berhasil dihapus"}, status=status.HTTP_204_NO_CONTENT)

    def log_activity(self, user_id, action, name_table, project, old_value=None, new_value=None):
        user_instance = get_object_or_404(User, id_user=user_id)
    
        object_data = {
            'id_project': project.id_project,
            'status': project.status,
            'requester': project.requester,
            'application_name': project.application_name,
            'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else None,
            'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
            'hld': str(project.hld),
            'lld': str(project.lld),
            'brd': project.brd,
            'sequence_number': project.sequence_number,
        }

        if old_value is not None and new_value is not None:
            object_data[name_table] = {
                'old': str(old_value),
                'new': str(new_value),
            }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

# Seluruh bagian komentar yang tidak digunakan telah saya hapus agar kode menjadi lebih bersih.
