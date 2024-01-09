# serializers.py
from rest_framework import serializers
from .models import Deliverable, ProjectCharter, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class DeliverableSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    
    # Mengatur status_deliverable menjadi read-only
    status_deliverable = serializers.CharField(read_only=True)

    class Meta:
        model = Deliverable
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, list):
            return [super(DeliverableSerializer, self).to_internal_value(item) for item in data]
        return super(DeliverableSerializer, self).to_internal_value(data)

    def validate(self, data):
        deliverables = data.get('deliverables', '')
        if deliverables:
            # Jika deliverables diisi, atur status_deliverable ke 'done'
            data['status_deliverable'] = 'done'
        else:
            # Jika deliverables kosong, atur status_deliverable ke 'draft'
            data['status_deliverable'] = 'draft'

        return data

class DeliverableListSerializer(serializers.ListSerializer):
    child = DeliverableSerializer()
