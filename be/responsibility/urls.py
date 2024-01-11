from django.urls import path
from .views import ResponsibilityListCreateAPIView, ResponsibilityDetailAPIView

urlpatterns = [
    path('bility/', ResponsibilityListCreateAPIView.as_view(), name='responsibility-list-create'),
    path('bility/<int:pk>/', ResponsibilityDetailAPIView.as_view(), name='responsibility-detail'),
]
    