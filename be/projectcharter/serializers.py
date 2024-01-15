from rest_framework import serializers
from .models import ProjectCharter, User, ActivityLog
import datetime
import json
from django.shortcuts import get_object_or_404

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

    def validate(self, data):
        project_name = data.get('project_name', '')
        project_manager = data.get('project_manager', '')
        customer = data.get('customer', '')
        end_customer = data.get('end_customer', '')
        bu_delivery = data.get('bu_delivery', '')
        bu_related = data.get('bu_related', '')
        project_description = data.get('project_description', '')
        id_user = data.get('id_user')

        # Tentukan field-field yang diperlukan
        required_fields = [project_name, project_manager, customer, end_customer, bu_delivery, bu_related, project_description]

        if any(field == '' for field in required_fields) or id_user is None:
            # Jika setidaknya satu field kosong atau id_user kosong, atur status_project ke 'draft'
            data['status_project'] = 'Draft'
        else:
            # Jika semua field terisi, atur status_project ke 'done'
            data['status_project'] = 'Done'

        return data


    def create(self, validated_data):
        # Hapus 'iwo' dari validated_data
        iwo = validated_data.pop('iwo', None)

        # Membuat objek model tanpa 'iwo'
        instance = super().create(validated_data)

        # Set 'iwo' ke objek model setelah objek dibuat
        instance.iwo = iwo
        instance.save()

        self.log_activity(instance.id_user.pk, 'created', 'Projectcharter', instance)

        return instance

    def get_iwo(self, instance):
        # Logika untuk menghasilkan nilai 'iwo'
        project_code = "SCC"
        customer_code = "INFO"
        sequence_number = instance.id_charter
        now = instance.createdAt
        year_month = now.strftime("%y%m")
        iwo = f"P-{year_month}{project_code.upper()}-{customer_code.upper()}{sequence_number:04d}"

        return iwo

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['iwo'] = self.get_iwo(instance)
        return data

    def update(self, instance, validated_data):
        # Update objek dengan nilai-nilai baru
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # List kolom yang harus diisi untuk mengatur status_project ke 'done'
        required_columns = ['project_name', 'project_manager', 'customer', 'end_customer', 'bu_delivery', 'bu_related', 'project_description', 'id_user']

        if all(getattr(instance, col) is not None for col in required_columns):
            # Jika semua field terisi, atur status_project ke 'done'
            instance.status_project = 'Done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_project ke 'draft'
            instance.status_project = 'Draft'

        instance.save()
        self.log_activity(instance.id_user.pk, 'updated', 'Projectcharter', instance)

        return instance

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

    def delete(self, request, *args, **kwargs):
        # Logging activity for deleted responsibility
        user_id = self.instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'projectcharter', self.instance)

        # Call the superclass delete method to perform the deletion
        return super().delete(request, *args, **kwargs)



class TotalProjectsSerializer(serializers.Serializer):
    total_projects = serializers.IntegerField()
    total_draft_projects = serializers.IntegerField()
    total_done_projects = serializers.IntegerField()
