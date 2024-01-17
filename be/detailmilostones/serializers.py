# serializers.py
from rest_framework import serializers
from .models import ProjectCharter, Description, SupportingDoc, Responsibility, Milostones, RoleResponsibilities, DetailResponsibilities, Deliverable, Approvedby, Status, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProjectCharterSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ProjectCharter
        fields = '__all__'

class DescriptionSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = ProjectCharterSerializer()

    class Meta:
        model = Description
        fields = '__all__'

class SupportingDocSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = ProjectCharterSerializer()

    class Meta:
        model = SupportingDoc
        fields = '__all__'

class ResponsibilitySerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = ProjectCharterSerializer()

    class Meta:
        model = Responsibility
        fields = '__all__'

class MilostonesSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = ProjectCharterSerializer()

    class Meta:
        model = Milostones
        fields = '__all__'

class RoleResponsibilitiesSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = ProjectCharterSerializer()

    class Meta:
        model = RoleResponsibilities
        fields = '__all__'

class DetailResponsibilitiesSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = ProjectCharterSerializer()
    id_responsibilities = RoleResponsibilitiesSerializer()

    class Meta:
        model = DetailResponsibilities
        fields = '__all__'

class DeliverableSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = ProjectCharterSerializer()

    class Meta:
        model = Deliverable
        fields = '__all__'

class ApprovedbySerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = ProjectCharterSerializer()

    class Meta:
        model = Approvedby
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    id_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_charter = serializers.PrimaryKeyRelatedField(queryset=ProjectCharter.objects.all())
    id_description = serializers.PrimaryKeyRelatedField(queryset=Description.objects.all())
    id_deliverable = serializers.PrimaryKeyRelatedField(queryset=Deliverable.objects.all())
    id_milostone = serializers.PrimaryKeyRelatedField(queryset=Milostones.objects.all())
    id_responsibilities = serializers.PrimaryKeyRelatedField(queryset=RoleResponsibilities.objects.all())
    id_responsibility = serializers.PrimaryKeyRelatedField(queryset=Responsibility.objects.all())
    id_supporting = serializers.PrimaryKeyRelatedField(queryset=SupportingDoc.objects.all())
    id_approv = serializers.PrimaryKeyRelatedField(queryset=Approvedby.objects.all())
    id_detail_roleresponsibilities = serializers.PrimaryKeyRelatedField(queryset=DetailResponsibilities.objects.all())

    class Meta:
        model = Status
        fields = '__all__'
