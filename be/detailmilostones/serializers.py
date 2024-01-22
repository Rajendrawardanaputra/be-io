from rest_framework import serializers
from .models import Status, ProjectCharter, Description, SupportingDoc, Responsibility, Milostones, RoleResponsibilities, DetailResponsibilities, Deliverable, Approvedby

class StatusSerializer(serializers.ModelSerializer):
    project_charter = serializers.CharField(source='id_charter.status_project', read_only=True)
    description = serializers.CharField(source='id_description.status_description', read_only=True)
    supportingdoc = serializers.CharField(source='id_supporting.status_supportingdoc', read_only=True)
    responsibility = serializers.CharField(source='id_responsibility.status_responsibility', read_only=True)
    milostones = serializers.CharField(source='id_milostone.status_milostones', read_only=True)
    responsibilities = serializers.CharField(source='id_responsibilities.status_responsibilities', read_only=True)
    detailresponsibilities = serializers.CharField(source='id_detail_roleresponsibilities.status_detailresponsibilities', read_only=True)
    deliverable = serializers.CharField(source='id_deliverable.status_deliverable', read_only=True)
    approvedby = serializers.CharField(source='id_approv.status_approvedby', read_only=True)

    class Meta:
        model = Status
        fields = '__all__'

    status = serializers.ReadOnlyField()
