from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Status
from .serializers import StatusSerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class StatusListCreateView(generics.ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
