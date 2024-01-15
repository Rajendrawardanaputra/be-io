# views.py

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DetailMainPower, ActivityLog
from .serializers import DetailMainPowerSerializer, DetailMainPowerListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
from rest_framework import status

class RoleListView(APIView):
    def get(self, request, *args, **kwargs):
        roles = [
            'PM/Scrum Master', 'Senior Business Analyst', 'Product Owner',
            'UI UX designer', 'Senior Programmer Backend', 'Senior Programmer FrontEnd',
            'Mobile Developer', 'Design Grafis', 'FullStack Developer',
            'DBA', 'DevOps', 'Business Analyst',
            'Junior Programmer Backend', 'Junior Programmer FrontEnd',
            'Technical Writer', 'Tester'
        ]

        return Response({'roles': roles}, status=status.HTTP_200_OK)

class DetailMainPowerListCreateView(generics.ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]

    queryset = DetailMainPower.objects.all()
    serializer_class = DetailMainPowerSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return DetailMainPowerListSerializer
        return DetailMainPowerSerializer

    def perform_create(self, serializer):
        instances = []

        for data in self.request.data:
            serializer_instance = DetailMainPowerSerializer(data=data)
            if serializer_instance.is_valid():
                instance = serializer_instance.save()
                total_man_rate = 0

                if 'man_days_rate' in data and 'man_power' in data and 'days' in data:
                    total_man_rate = instance.man_days_rate * instance.man_power * instance.days

                instance.total_man_rate = total_man_rate
                instance.save()

                # Membuat log aktivitas untuk pembuatan objek
                ActivityLog.objects.create(
                    id_user=instance.id_user,
                    action='create',
                    name_table='DetailMainPower',
                    object=str(instance),
                    name_column='total_man_rate',
                    changes=str(total_man_rate)
                )

                instances.append(instance)

        serializer.instance = instances
        response_data = {
            'message': 'Data berhasil dibuat',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Tambahkan kemampuan pencarian berdasarkan id_project
        id_project = self.request.query_params.get('id_project')
        if id_project:
            queryset = queryset.filter(id_project=id_project)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'message': 'Data berhasil diambil',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class DetailMainPowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]

    queryset = DetailMainPower.objects.all()
    serializer_class = DetailMainPowerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'message': 'Data berhasil diambil',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        total_man_rate = 0
        if 'man_days_rate' in request.data and 'man_power' in request.data and 'days' in request.data:
            total_man_rate = instance.man_days_rate * instance.man_power * instance.days

        # Membuat log aktivitas untuk pembaruan objek
        ActivityLog.objects.create(
            id_user=instance.id_user,
            action='update',
            name_table='DetailMainPower',
            object=str(instance),
            name_column='total_man_rate',
            changes=str(total_man_rate)
        )

        response_data = {
            'message': 'Data berhasil diperbarui',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Membuat log aktivitas untuk penghapusan objek
        ActivityLog.objects.create(
            id_user=instance.id_user,
            action='delete',
            name_table='DetailMainPower',
            object=str(instance),
            name_column='total_man_rate',
            changes=str(instance.total_man_rate)
        )

        self.perform_destroy(instance)
        response_data = {'message': 'Data berhasil dihapus'}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
