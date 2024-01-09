from rest_framework import serializers
from .models import ProjectCharter, User
import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True)
    iwo = serializers.SerializerMethodField()

    class Meta:
        model = ProjectCharter
        fields = '__all__'
        read_only_fields = ['status_project', 'iwo']


    def create(self, validated_data):
        # Hapus 'iwo' dari validated_data
        iwo = validated_data.pop('iwo', None)

        # Membuat objek model tanpa 'iwo'
        instance = super().create(validated_data)

        # Set 'iwo' ke objek model setelah objek dibuat
        instance.iwo = iwo
        instance.save()

        return instance
    
    def get_iwo(self, instance):
        project_code = "SCC"  # Example project code, you can customize this
        customer_code = "INFO"  # Example customer code, you can customize this

        # Assuming id_charter is unique and can be used as a sequence number
        sequence_number = instance.id_charter
        now = instance.createdAt
        year_month = now.strftime("%y%m")
        iwo = f"P-{year_month}{project_code.upper()}-{customer_code.upper()}{sequence_number:04d}"

        return iwo

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['iwo'] = self.get_iwo(instance)
        return data
    
  

class TotalProjectsSerializer(serializers.Serializer):
    total_projects = serializers.IntegerField()
    total_draft_projects = serializers.IntegerField()
    total_done_projects = serializers.IntegerField()
