from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectCharter
from .serializers import ProjectCharterSerializer, TotalProjectsSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
from rest_framework.views import APIView
import datetime

class TotalProjectsAPIView(ListAPIView):
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
        serializer.save()

        # Return the object instance
        return serializer.instance

class ProjectCharterDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    
    queryset = ProjectCharter.objects.all()
    serializer_class = ProjectCharterSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check if at least one column is empty
        if any(value == "" for value in serializer.validated_data.values()):
            serializer.validated_data['status_project'] = 'draft'
        else:
            serializer.validated_data['status_project'] = 'done'

        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

   