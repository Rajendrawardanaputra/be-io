# views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import SupportingDoc, ActivityLog, User
from .serializers import SupportingDocSerializer
import boto3
from datetime import datetime
from django.conf import settings
from rest_framework import serializers
from be.middleware.token_middleware import CustomJWTAuthentication
from django.shortcuts import get_object_or_404
import json
from django.conf import settings

class SupportingDocListView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = SupportingDoc.objects.all()
    serializer_class = SupportingDocSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        file_document = validated_data.get('document')

        if file_document:
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

            s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            file_document_name = f"document/{current_datetime}_{file_document.name}"
            file_document_url = f"/internalorder/{file_document_name}"

            serializer.save(document=file_document_url, status_supportingdoc='done')

            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=file_document_name, Body=file_document.read(), ContentType=file_document.content_type)

            # Memanggil log_activity dengan informasi yang sesuai
            self.log_activity(serializer.validated_data.get('id_user').id_user, 'created', serializer.instance)

            return Response({"message": "Document diunggah", "document": file_document_url}, status=status.HTTP_201_CREATED)
        else:
            status_supportingdoc = 'draft' if any(value in [None, ""] for key, value in validated_data.items() if key != 'status_supportingdoc') else 'done'
            serializer.save(status_supportingdoc=status_supportingdoc)

            # Memanggil log_activity dengan informasi yang sesuai
            self.log_activity(serializer.validated_data.get('id_user').id_user, 'created', serializer.instance)

            return Response({"message": "Objek Description dibuat tanpa file document"}, status=status.HTTP_201_CREATED)
        
    def log_activity(self, user_id, action, supporting):
         user_instance = get_object_or_404(User, id_user=user_id)
         object_data = {
            'document_name': supporting.document_name,
            'notes': supporting.notes,
            'document_url': supporting.document.url if supporting.document else None,
        }

         ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table='SupportingDoc',
            object=json.dumps(object_data),
        )


class SupportingDocDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = SupportingDoc.objects.all()
    serializer_class = SupportingDocSerializer

    def perform_update(self, serializer):
     old_file_document = serializer.instance.document
     new_file_document = self.request.data.get('document')
     data = {}

     if new_file_document is not None and hasattr(new_file_document, 'size'):
        # Validasi tipe file
        valid_file_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'image/jfif']
        if new_file_document.content_type not in valid_file_types:
            raise serializers.ValidationError("Tipe file tidak valid. Harap unggah file PDF, JPEG, PNG, JFIF, atau GIF.")
        
        s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        new_file_name = f"document/{current_datetime}_{new_file_document.name}"
        file_document = f"/internalorder/{new_file_name}"

        # Simpan file baru ke S3
        s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
            Key=new_file_name, Body=new_file_document, ContentType=new_file_document.content_type)

        # Hapus file lama dari S3
        if old_file_document:
            # Dapatkan nama file dari atribut name
            old_file_name = old_file_document.name.split('/')[-1]
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).delete_objects(Delete={'Objects': [{'Key': f'document/{old_file_name}'}]})

        data["document"] = file_document  # Tambahkan data document ke dictionary

    # Menambahkan logika untuk mengatasi document yang tidak ingin diubah
     elif old_file_document:
        data["document"] = old_file_document.url  # Menggunakan url untuk document

    # Cek apakah ada kolom lain yang kosong atau None, kecuali status_supportingdoc dan document
     if any(value in [None, ""] for key, value in serializer.validated_data.items() if key not in ['status_supportingdoc', 'document']):
        serializer.validated_data['status_supportingdoc'] = 'draft'
     else:
        serializer.validated_data['status_supportingdoc'] = 'done'

     serializer.save(**data)

    # Menambahkan log activity untuk update
     self.log_activity(serializer.instance.id_user.pk, 'updated', 'SupportingDoc', serializer.instance)

    def perform_destroy(self, instance):
        # Menambahkan log activity untuk delete
        self.log_activity(instance.id_user.pk, 'deleted', 'SupportingDoc', instance)
        instance.delete()

    def log_activity(self, user_id, action, SupportingDoc, supporting):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'document_name': supporting.document_name,
            'notes': supporting.notes,
            'document_url': supporting.document.url if supporting.document else None,
            # ... (Tambahkan kolom lainnya jika diperlukan)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=SupportingDoc,
            object=json.dumps(object_data),
        )