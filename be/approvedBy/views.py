# views.py
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Approvedby
from .serializers import ApprovedbySerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class ApprovedbyListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication] 
    queryset = Approvedby.objects.all()
    serializer_class = ApprovedbySerializer


class ApprovedbyDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Approvedby.objects.all()
    serializer_class = ApprovedbySerializer
