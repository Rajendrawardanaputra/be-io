from django.urls import path
from .views import ProjectCharterListCreateAPIView, ProjectCharterDetailAPIView, TotalProjectsAPIView

urlpatterns = [
    path('projectcharter/', ProjectCharterListCreateAPIView.as_view(), name='detail_main_power_list_create'),
    path('projectcharter/<int:pk>/', ProjectCharterDetailAPIView.as_view(), name='detail_main_power_detail'),
    path('totalcharter/', TotalProjectsAPIView.as_view(), name='total_projects'),
]