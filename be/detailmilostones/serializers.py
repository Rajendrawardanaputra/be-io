# from rest_framework import serializers
# from .models import Status, User, ProjectCharter, DetailResponsibilities, Description, Responsibility, Milostones, RoleResponsibilities, Deliverable, Approvedby



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['nama']

# class ProjectCharterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectCharter
#         fields = ['status_project']

# class DetailResponsibilitiesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DetailResponsibilities
#         fields = ['status_detailresponsibilities']
# class DescriptionSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Description
#         fields = ['status_description']
# class ResponsibilitySerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Responsibility
#         fields = ['status_responsibility']
# class MilostonesSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Milostones
#         fields = ['status_milostones']

# class RoleResponsibilitiesSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = RoleResponsibilities
#         fields = ['status_responsibilities']

# class DeliverableSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Deliverable
#         fields = ['status_deliverable']

# class ApprovedbySerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Approvedby
#         fields = ['status_approvedby']

# class StatusSerializer(serializers.ModelSerializer):
#     user = UserSerializer(source='id_user', read_only=True) 
#     project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
#     detailresponsibilities = DetailResponsibilitiesSerializer(source='id_detail_roleresponsibilities', read_only=True)
#     description = DescriptionSerializer(source='id_description', read_only=True)
#     responsibility = ResponsibilitySerializer(source='id_responsibility', read_only=True)
#     milostones = MilostonesSerializer(source='id_milostone', read_only=True)
#     responsibilites = RoleResponsibilitiesSerializer(source='id_responsibilities', read_only=True)
#     deliverable = DeliverableSerializer(source='id_deliverable', read_only=True)
#     approvedby = ApprovedbySerializer(source='id_approv', read_only=True)

#     class Meta:
#         model = Status
#         fields = '__all__'
