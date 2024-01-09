from django.urls import path
from .views import RoleResponsibilitiesListView, RoleResponsibilitiesDetailView

urlpatterns = [
    path('rolerespon/', RoleResponsibilitiesListView.as_view(), name='description-list'),
    path('rolerespon/<int:pk>/', RoleResponsibilitiesDetailView.as_view(), name='description-detail'),
]