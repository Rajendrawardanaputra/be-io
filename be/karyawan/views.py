from rest_framework.generics import ListAPIView
from rest_framework import permissions
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class ActivityLogListView(ListAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer  # Adjust as needed
