from rest_framework.generics import ListAPIView
from rest_framework import permissions
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class ActivityLogListView(ListAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        # Mendapatkan id_user dari parameter query
        id_user = self.request.query_params.get('id_user')

        # Mengembalikan entri ActivityLog hanya untuk id_user tertentu
        if id_user:
            return ActivityLog.objects.filter(id_user=id_user)
        else:
            return ActivityLog.objects.all()
