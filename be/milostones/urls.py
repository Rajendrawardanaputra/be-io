# urls.py
from django.urls import path
from .views import MilostonesListCreateAPIView, MilostonesDetailAPIView

urlpatterns = [
    path('milostones/', MilostonesListCreateAPIView.as_view(), name='detail_main_power_list_create'),
    path('milostones/<int:pk>/', MilostonesDetailAPIView.as_view(), name='detail_main_power_detail'),
]
