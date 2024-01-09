# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Responsibility
from .serializers import ResponsibilitySerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class ResponsibilityViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer

    def perform_create(self, serializer):
        self.set_status(serializer)
        serializer.save()
        response_data = {'message': 'Responsibility created successfully', 'data': serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        self.set_status(serializer)
        serializer.save()
        response_data = {'message': 'Responsibility updated successfully', 'data': serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)

    def set_status(self, serializer):
        fields_to_check = ['pm_responsibility', 'project_value', 'start_date', 'end_date', 'id_charter', 'id_user']
        is_draft = any([serializer.validated_data[field] in [None, ""] for field in fields_to_check])
        serializer.validated_data['status_responsibility'] = 'draft' if is_draft else 'done'
