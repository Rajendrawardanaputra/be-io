# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DetailMilostonesViewSet

router = DefaultRouter()
router.register(r'detailmilostones', DetailMilostonesViewSet, basename='detail_milostones')

urlpatterns = [
    path('', include(router.urls)),
]
