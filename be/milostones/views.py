from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Milostones
from .serializers import MilostonesSerializer, MilostonesListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class MilostonesListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Milostones.objects.all()
    serializer_class = MilostonesSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return MilostonesListSerializer
        return MilostonesSerializer

class MilostonesDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Milostones.objects.all()
    serializer_class = MilostonesSerializer

