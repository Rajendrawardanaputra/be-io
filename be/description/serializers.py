# serializers.py
from rest_framework import serializers
from .models import Description, ProjectCharter, User, ActivityLog
import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class DescriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    
    class Meta:
        model = Description
        fields = '__all__'
        read_only_fields = ['status_description']


    def validate(self, data):
        hlr = data.get('hlr', '')
        assumptions = data.get('assumptions', '')
        contraints = data.get('contraint', '')
        risk = data.get('risk', '')
        key_stakeholders = data.get('key_stakeholders', '')
        id_charter = data.get('id_charter')
        id_user = data.get('id_user')

        if hlr and assumptions and contraints and risk and key_stakeholders and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            data['status_description'] = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            data['status_description'] = 'draft'

        return data
    
    def create(self, validated_data):
        description = super().create(validated_data)

        hlr = description.hlr
        assumptions = description.assumptions
        contraints = description.contraints
        risk = description.risk
        key_stakeholders = description.key_stakeholders
        id_charter = description.id_charter
        id_user = description.id_user_id

        if hlr and assumptions and contraints and risk and key_stakeholders and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            description.status_description = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            description.status_description = 'draft'

        description.save()
        self.log_activity(description.id_user.pk, 'created', 'Description', description)
        return description
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        hlr = instance.hlr
        assumptions = instance.assumptions
        contraints = instance.contraints
        risk = instance.risk
        key_stakeholders = instance.key_stakeholders
        id_charter = instance.id_charter
        id_user = instance.id_user_id

        if hlr and assumptions and contraints and risk and key_stakeholders and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_supportingdoc ke 'done'
            instance.status_description = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_supportingdoc ke 'draft'
            instance.status_description = 'draft'

        instance.save()
        self.log_activity(instance.id_user.id_user, 'updated', 'Description', instance)
        return instance
    
    def log_activity(self, user_id, action, name_table, description):
        object_data = {
            'hlr': description.hlr.url if description.hlr else None, # Convert date to string 
            'assumptions': description.assumptions,
            'contraints': description.contraints,
            'risk': description.risk,
            'key_stakeholders': description.key_stakeholders,

            
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user_id=user_id,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

    def delete(self, instance):
        user_id = instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'description', instance)
        instance.delete()
