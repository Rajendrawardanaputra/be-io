# views.py
from rest_framework import generics
from .models import Status, ProjectCharter, Description, SupportingDoc, Responsibility, Milostones, RoleResponsibilities, DetailResponsibilities
from .serializers import StatusSerializer, ProjectCharterSerializer, DescriptionSerializer, SupportingDocSerializer, ResponsibilitySerializer, MilostonesSerializer, RoleResponsibilitiesSerializer, DetailResponsibilitiesSerializer
from rest_framework.response import Response
from rest_framework import status

class OverallStatusView(generics.RetrieveAPIView):
    serializer_class = StatusSerializer

    def get_object(self):
        # Ambil semua data dari setiap model
        project_charter = ProjectCharter.objects.all()
        descriptions = Description.objects.all()
        supporting_docs = SupportingDoc.objects.all()
        responsibilities = Responsibility.objects.all()
        milostones = Milostones.objects.all()
        role_responsibilities = RoleResponsibilities.objects.all()
        detail_responsibilities = DetailResponsibilities.objects.all()

        # Tentukan status keseluruhan
        overall_status = 'done'

        for model_data in [project_charter, descriptions, supporting_docs, responsibilities, milostones, role_responsibilities, detail_responsibilities]:
            for data in model_data:
                if data.status.lower() == 'draft':
                    overall_status = 'draft'
                    break

        # Buat objek status baru
        status_object = Status(status=overall_status)
        return status_object
