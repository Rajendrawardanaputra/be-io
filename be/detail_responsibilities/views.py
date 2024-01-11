from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import DetailResponsibilities, User, ActivityLog
from .serializers import DetailResponsibilitiesSerializer, DetailResponsibilitiesListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
import json
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class DetailResponsibilitiesListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = DetailResponsibilities.objects.all()
    serializer_class = DetailResponsibilitiesSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return DetailResponsibilitiesListSerializer
        return DetailResponsibilitiesSerializer

    def perform_create(self, serializer):
        detailresponbilities_list = serializer.save()

        for detailresponbilities in detailresponbilities_list:
            # Logging activity for each milostones
            user_id = detailresponbilities.id_user.id_user
            self.log_activity(user_id, 'created', 'Detailresponbilities', detailresponbilities)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def log_activity(self, user_id, action, name_table, detailresponbilities, new_photo=None, old_photo=None):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'nama_pc': detailresponbilities.nama_pc,
            'role_pc': detailresponbilities.role_pc,
            'description': detailresponbilities.description,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class DetailResponsibilitiesDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = DetailResponsibilities.objects.all()
    serializer_class = DetailResponsibilitiesSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_detailresponbilities = serializer.save()

        # Logging activity for updated milostones
        user_id = updated_detailresponbilities.id_user.id_user
        self.log_activity(user_id, 'updated', 'Detailresponbilities', updated_detailresponbilities)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Logging activity for deleted milostones
        user_id = instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'Detailresponbilities', instance)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def log_activity(self, user_id, action, name_table, detailresponbilities, new_photo=None, old_photo=None):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'nama_pc': detailresponbilities.nama_pc,
            'role_pc': detailresponbilities.role_pc,
            'description': detailresponbilities.description,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )