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

    def get_queryset(self):
        id_charter = self.request.query_params.get('id_charter', None)
        queryset = DetailResponsibilities.objects.all()

        if id_charter:
            queryset = queryset.filter(id_charter=id_charter)

        return queryset

    def perform_create(self, serializer):
        detailresponsibilities_list = serializer.save()

        for detailresponsibilities in detailresponsibilities_list:
            user_id = detailresponsibilities.id_user.id_user
            self.log_activity(user_id, 'created', 'DetailResponsibilities', detailresponsibilities)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def log_activity(self, user_id, action, name_table, detailresponsibilities):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'nama_pc': detailresponsibilities.nama_pc,
            'role_pc': detailresponsibilities.role_pc,
            'description': detailresponsibilities.description,
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
        updated_detailresponsibilities = serializer.save()

        user_id = updated_detailresponsibilities.id_user.id_user
        self.log_activity(user_id, 'updated', 'DetailResponsibilities', updated_detailresponsibilities)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        user_id = instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'DetailResponsibilities', instance)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def log_activity(self, user_id, action, name_table, detailresponsibilities):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'nama_pc': detailresponsibilities.nama_pc,
            'role_pc': detailresponsibilities.role_pc,
            'description': detailresponsibilities.description,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )
