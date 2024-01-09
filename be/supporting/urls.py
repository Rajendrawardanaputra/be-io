from django.urls import path
from .views import SupportingDocListView, SupportingDocDetailView

urlpatterns = [
    path('supporting/', SupportingDocListView.as_view(), name='description-list'),
    path('supporting/<int:pk>/', SupportingDocDetailView.as_view(), name='description-detail'),
]