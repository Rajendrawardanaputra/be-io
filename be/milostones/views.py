# views.py
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Milostones, User, ActivityLog
from .serializers import MilostonesSerializer, MilostonesListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
import json
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class MilostonesListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Milostones.objects.all()
    serializer_class = MilostonesSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return MilostonesListSerializer
        return MilostonesSerializer

    def perform_create(self, serializer):
        milostones_list = serializer.save()

        for milostones in milostones_list:
            # Logging activity for each milostones
            user_id = milostones.id_user.id_user
            self.log_activity(user_id, 'created', 'Milostones', milostones)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def log_activity(self, user_id, action, name_table, milostones, new_photo=None, old_photo=None):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'tanggal': milostones.tanggal,
            'milestone': milostones.milestone,
            'deskripsi': milostones.deskripsi,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class MilostonesDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Milostones.objects.all()
    serializer_class = MilostonesSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_milostones = serializer.save()

        # Logging activity for updated milostones
        user_id = updated_milostones.id_user.id_user
        self.log_activity(user_id, 'updated', 'Milostones', updated_milostones)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Logging activity for deleted milostones
        user_id = instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'Milostones', instance)

        instance.delete()
        return Response({"message": "Objek berhasil dihapus"}, status=status.HTTP_204_NO_CONTENT)

    def log_activity(self, user_id, action, name_table, milostones, new_photo=None, old_photo=None):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'milestone': milostones.milestone,
            'deskripsi': milostones.deskripsi,
            'tanggal': milostones.tanggal,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )