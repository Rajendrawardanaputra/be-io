# views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Deliverable, User, ActivityLog
from .serializers import DeliverableSerializer, DeliverableListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
import json
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class DeliverableListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Deliverable.objects.all()
    serializer_class = DeliverableSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return DeliverableListSerializer
        return DeliverableSerializer
    
    def perform_create(self, serializer):
        deliverables_list = serializer.save()

        for deliverables in deliverables_list:
            # Logging activity for each deliverable
            user_id = deliverables.id_user.id_user
            self.log_activity(user_id, 'created', 'Deliverables', deliverables)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def log_activity(self, user_id, action, name_table, deliverables):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'deliverables': deliverables.deliverables,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class DeliverableDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Deliverable.objects.all()
    serializer_class = DeliverableSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_deliverables = serializer.save()

        # Logging activity for updated deliverable
        user_id = updated_deliverables.id_user.id_user
        self.log_activity(user_id, 'updated', 'Deliverables', updated_deliverables)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Calling delete method in serializer
        instance_serializer = self.get_serializer(instance)
        instance_serializer.delete(instance)

        return Response({"message": "Objek berhasil dihapus"}, status=status.HTTP_204_NO_CONTENT)

    def log_activity(self, user_id, action, name_table, deliverables):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'deliverables': deliverables.deliverables,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )
