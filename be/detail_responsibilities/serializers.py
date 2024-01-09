from rest_framework import serializers
from .models import DetailResponsibilities, ProjectCharter, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class DetailResponsibilitiesSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    status_detailresponsibilities = serializers.CharField(read_only=True)
    
    class Meta:
        model = DetailResponsibilities
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, list):
            return [super(DetailResponsibilitiesSerializer, self).to_internal_value(item) for item in data]
        return super(DetailResponsibilitiesSerializer, self).to_internal_value(data)
    
    def validate(self, data):
        nama_pc = data.get('nama_pc', '')
        role_pc = data.get('role_pc', '')
        description = data.get('description', '')
        id_responsibilities = data.get('id_responsibilities')
        id_charter = data.get('id_charter')
        id_user = data.get('id_user')

        if nama_pc and role_pc and description and id_responsibilities is not None and id_charter is not None  and id_user is not None:
            data['status_detailresponsibilities'] = 'done'
        else:
            data['status_detailresponsibilities'] = 'draft'

        return data
     
class DetailResponsibilitiesListSerializer(serializers.ListSerializer):
    child = DetailResponsibilitiesSerializer()
