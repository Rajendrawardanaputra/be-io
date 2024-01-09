from django.shortcuts import render

# Create your views her# views.py
from rest_framework import viewsets
from .models import DetailMilostones
from .serializers import DetailMilostonesSerializer

class DetailMilostonesViewSet(viewsets.ModelViewSet):
    queryset = DetailMilostones.objects.all()
    serializer_class = DetailMilostonesSerializer

