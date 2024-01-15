from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Responsibility, User, ActivityLog
from .serializers import ResponsibilitySerializer
from be.middleware.token_middleware import CustomJWTAuthentication
import json

class ResponsibilityListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer

    def get_queryset(self):
        id_charter = self.request.query_params.get('id_charter', None)
        queryset = super().get_queryset()
        if id_charter:
            queryset = queryset.filter(id_charter=id_charter)
        return queryset

    def perform_create(self, serializer):
        responsibility = serializer.save()
        serializer.log_activity(responsibility.id_user.pk, 'created', 'Responsibility', responsibility)
        response_data = {'message': 'Responsibility created successfully', 'data': serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED)

class ResponsibilityDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer

    def perform_update(self, serializer):
        updated_responsibility = serializer.save()
        serializer.log_activity(updated_responsibility.id_user.pk, 'updated', 'Responsibility', updated_responsibility)
        response_data = {'message': 'Responsibility updated successfully', 'data': serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        # Logging activity for deleted responsibility
        serializer = self.get_serializer(instance)
        serializer.log_activity(instance.id_user.id_user, 'deleted', 'Responsibility', instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
