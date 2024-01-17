# views.py
from rest_framework import generics
from .models import Status, ProjectCharter, Description, SupportingDoc, Responsibility, Milostones, RoleResponsibilities, DetailResponsibilities, Deliverable, Approvedby, User
from .serializers import StatusSerializer, UserSerializer, ProjectCharterSerializer, DescriptionSerializer, SupportingDocSerializer, ResponsibilitySerializer, MilostonesSerializer, RoleResponsibilitiesSerializer, DetailResponsibilitiesSerializer, DeliverableSerializer, ApprovedbySerializer

class StatusList(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_serializer_context(self):
        context = super(StatusList, self).get_serializer_context()
        # Tambahan context untuk setiap model yang digunakan dalam Status
        context['project_charter'] = ProjectCharter.objects.all()
        context['description'] = Description.objects.all()
        context['supporting_doc'] = SupportingDoc.objects.all()
        context['responsibility'] = Responsibility.objects.all()
        context['milostones'] = Milostones.objects.all()
        context['role_responsibilities'] = RoleResponsibilities.objects.all()
        context['detail_responsibilities'] = DetailResponsibilities.objects.all()
        context['deliverable'] = Deliverable.objects.all()
        context['approvedby'] = Approvedby.objects.all()
        context['user'] = User.objects.all()
        return context
