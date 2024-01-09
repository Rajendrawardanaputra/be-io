from django.urls import path
from .views import ProjectInternalListCreateView, ProjectInternalRetrieveUpdateDestroyView

urlpatterns = [
    path('projectinternal/', ProjectInternalListCreateView.as_view(), name='project_internal-list-create'),
    path('projectinternal/<int:pk>/', ProjectInternalRetrieveUpdateDestroyView.as_view(), name='project_internal-retrieve-update-destroy'),
]
