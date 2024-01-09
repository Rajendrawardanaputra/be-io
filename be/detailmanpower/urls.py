from django.urls import path
from .views import DetailMainPowerListCreateView, DetailMainPowerDetailView, RoleListView

urlpatterns = [
    path('detailmainpower/', DetailMainPowerListCreateView.as_view(), name='detail_main_power_list_create'),
    path('detailmainpower/<int:pk>/', DetailMainPowerDetailView.as_view(), name='detail_main_power_detail'),
    path('roles/', RoleListView.as_view(), name='role-list')
]
