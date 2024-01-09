# views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Deliverable
from .serializers import DeliverableSerializer, DeliverableListSerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class DeliverableListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]

    queryset = Deliverable.objects.all()
    serializer_class = DeliverableSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return DeliverableListSerializer
        return DeliverableSerializer

class DeliverableDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Deliverable.objects.all()
    serializer_class = DeliverableSerializer