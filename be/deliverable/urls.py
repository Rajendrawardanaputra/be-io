from django.urls import path
from .views import DeliverableListCreateAPIView, DeliverableDetailAPIView

urlpatterns = [
    path('deliverable/', DeliverableListCreateAPIView.as_view(), name='detail_main_power_list_create'),
    path('deliverable/<int:pk>/', DeliverableDetailAPIView.as_view(), name='detail_main_power_detail'),
]