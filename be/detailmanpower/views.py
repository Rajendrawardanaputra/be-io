from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DetailMainPower
from .serializers import DetailMainPowerSerializer, DetailMainPowerListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
from rest_framework import status  # Tambahkan import ini


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

                # Periksa apakah bidang-bidang yang diperlukan diisi sebelum menghitung total_man_rate
                if 'man_days_rate' in data and 'man_power' in data and 'days' in data:
                    total_man_rate = instance.man_days_rate * instance.man_power * instance.days

                instance.total_man_rate = total_man_rate
                instance.save()

                instances.append(instance)

        serializer.instance = instances

        # Tambahkan respon JSON setelah membuat instance
        response_data = {
            'message': 'Data berhasil dibuat',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Tambahkan respon JSON pada metode list
        response_data = {
            'message': 'Data berhasil diambil',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class DetailMainPowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    
    queryset = DetailMainPower.objects.all()
    serializer_class = DetailMainPowerSerializer

    # Tambahkan respon JSON pada metode retrieve
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            'message': 'Data berhasil diambil',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # Tambahkan respon JSON pada metode update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {
            'message': 'Data berhasil diperbarui',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # Tambahkan respon JSON pada metode destroy
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {'message': 'Data berhasil dihapus'}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
