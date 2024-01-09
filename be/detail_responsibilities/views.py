from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import DetailResponsibilities
from .serializers import DetailResponsibilitiesSerializer, DetailResponsibilitiesListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class DetailResponsibilitiesListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = DetailResponsibilities.objects.all()
    serializer_class = DetailResponsibilitiesSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return DetailResponsibilitiesListSerializer
        return DetailResponsibilitiesSerializer

class DetailResponsibilitiesDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = DetailResponsibilities.objects.all()
    serializer_class = DetailResponsibilitiesSerializer
