# urls.py
from django.urls import path
from .views import DetailResponsibilitiesListCreateAPIView, DetailResponsibilitiesDetailAPIView

urlpatterns = [
    path('detailrespon/', DetailResponsibilitiesListCreateAPIView.as_view(), name='detail_main_power_list_create'),
    path('detailrespon/<int:pk>/',DetailResponsibilitiesDetailAPIView.as_view(), name='detail_main_power_detail'),
]
