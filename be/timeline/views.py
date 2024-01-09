from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import DetailTimeline
from .serializers import DetailTimelineSerializer, DetailTimelineListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication
# from jwt import ExpiredSignatureError, InvalidTokenError
# from django.http import JsonResponse

class DetailTimelineListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]

    queryset = DetailTimeline.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return DetailTimelineListSerializer
        return DetailTimelineSerializer

    def get_serializer(self, *args, **kwargs):
        # Mengatasi AssertionError dengan menambahkan fields untuk project_internal
        if 'fields' not in kwargs and self.get_serializer_class() == DetailTimelineListSerializer:
            kwargs['context'] = {'fields': ['user', 'project_internal', 'weeks', 'activity']}
        return super().get_serializer(*args, **kwargs)



class DetailTimelineDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    
    queryset = DetailTimeline.objects.all()
    serializer_class = DetailTimelineSerializer

    def get_serializer(self, *args, **kwargs):
        # Mengatasi AssertionError dengan menambahkan fields untuk project_internal
        if 'fields' not in kwargs and self.serializer_class == DetailTimelineListSerializer:
            kwargs['context'] = {'fields': ['user', 'project_internal', 'weeks', 'activity']}
        return super().get_serializer(*args, **kwargs)
    

    
