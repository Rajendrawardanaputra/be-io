from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectCharter, User, ActivityLog
from .serializers import ProjectCharterSerializer, TotalProjectsSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
from rest_framework.views import APIView
import datetime
import json
from django.shortcuts import get_object_or_404

class TotalProjectsAPIView(ListAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = TotalProjectsSerializer

    def get(self, request, *args, **kwargs):
        total_projects = ProjectCharter.objects.count()
        total_draft_projects = ProjectCharter.objects.filter(status_project='draft').count()
        total_done_projects = ProjectCharter.objects.filter(status_project='done').count()

        data = {
            'total_projects': total_projects,
            'total_draft_projects': total_draft_projects,
            'total_done_projects': total_done_projects,
        }

        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ProjectCharterListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]

    queryset = ProjectCharter.objects.all()
    serializer_class = ProjectCharterSerializer

    def create(self, request, *args, **kwargs):
        # Create the serializer with request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Call perform_create to handle additional logic and return the instance
        instance = self.perform_create(serializer)

        # Now, you can add 'iwo' directly to the response data
        response_data = serializer.data
        response_data['iwo'] = instance.iwo

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data

        # Check if at least one column is empty
        if any(value == "" for value in validated_data.values()):
            validated_data['status_project'] = 'draft'
        else:
            validated_data['status_project'] = 'done'

        # Generate IWO dynamically
        project_code = "SCC"  # Example project code, you can customize this
        customer_code = "INFO"  # Example customer code, you can customize this
        sequence_number = ProjectCharter.objects.count() + 1  # You may need to adjust this based on your actual requirements

        now = datetime.datetime.now()
        year_month = now.strftime("%y%m")
        iwo = f"P-{year_month}{project_code.upper()}-{customer_code.upper()}{sequence_number:04d}"

        # Set IWO to the serializer data
        validated_data['iwo'] = iwo

        # Save the serializer, which returns the instance
        projectcharter = serializer.save()

        # Log the activity
        self.log_activity(projectcharter.id_user.pk, 'created', 'Projectcharter', projectcharter)

        # Return the object instance
        return projectcharter
    
    def log_activity(self, user_id, action, name_table, projectcharter):
        user_instance = get_object_or_404(User, id_user=user_id)
        object_data = {
            'project_name': projectcharter.project_name,
            'project_manager': projectcharter.project_manager,
            'customer': projectcharter.customer,
            'end_customer': projectcharter.end_customer,
            'bu_delivery': projectcharter.bu_delivery,
            'bu_related': projectcharter.bu_related,
            'project_description': projectcharter.project_description,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )


class ProjectCharterDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = ProjectCharter.objects.all()
    serializer_class = ProjectCharterSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Perbarui objek dengan nilai-nilai baru
        for key, value in serializer.validated_data.items():
            setattr(instance, key, value)

        # Tentukan kolom yang harus diisi untuk mengatur status_project ke 'done'
        required_columns = ['project_name', 'project_manager', 'customer', 'end_customer', 'bu_delivery', 'bu_related', 'project_description']

        if all(getattr(instance, col) != "" for col in required_columns):
            # Jika semua field terisi, atur status_project ke 'done'
            instance.status_project = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_project ke 'draft'
            instance.status_project = 'draft'

        instance.save()

        # Log aktivitas update
        self.log_activity(instance.id_user.pk, 'updated', 'Projectcharter', instance)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)

        self.log_activity(instance.id_user.pk, 'deleted', 'Projectcharter', instance)

        return Response({'message': 'Data deleted successfully'})


    def log_activity(self, user_id, action, name_table, projectcharter):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'project_name': projectcharter.project_name,
            'project_manager': projectcharter.project_manager,
            'customer': projectcharter.customer,
            'end_customer': projectcharter.end_customer,
            'bu_delivery': projectcharter.bu_delivery,
            'bu_related': projectcharter.bu_related,
            'project_description': projectcharter.project_description,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )
