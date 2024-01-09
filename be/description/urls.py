from django.urls import path
from .views import DescriptionListView, DescriptionDetailView

urlpatterns = [
    path('description/', DescriptionListView.as_view(), name='description-list'),
    path('description/<int:pk>/', DescriptionDetailView.as_view(), name='description-detail'),
]