# serializers.py
from rest_framework import serializers
from .models import Milostones, ProjectCharter, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nama']

class ProjectCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCharter
        fields = ['project_name']

class MilostonesSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user', read_only=True) 
    project_charter = ProjectCharterSerializer(source='id_charter', read_only=True)
    status_milostones = serializers.CharField(read_only=True)

    class Meta:
        model = Milostones
        fields = '__all__'

    def validate(self, data):
        milestone = data.get('milestone', '')
        deskripsi = data.get('deskripsi', '')
        tanggal = data.get('tanggal', '')
        id_charter = data.get('id_charter')
        id_user = data.get('id_user')

        if milestone and deskripsi and tanggal and id_charter is not None and id_user is not None:
            # Jika semua field terisi, atur status_milostones ke 'done'
            data['status_milostones'] = 'done'
        else:
            # Jika ada setidaknya satu field yang kosong, atur status_milostones ke 'draft'
            data['status_milostones'] = 'draft'

        return data

class MilostonesListSerializer(serializers.ListSerializer):
    child = MilostonesSerializer()
