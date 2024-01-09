from django.urls import path
from .views import ApprovedbyListCreateAPIView, ApprovedbyDetailAPIView

urlpatterns = [
    path('approved/', ApprovedbyListCreateAPIView.as_view(), name='detail_main_power_list_create'),
    path('approved/<int:pk>/', ApprovedbyDetailAPIView.as_view(), name='detail_main_power_detail'),
]
