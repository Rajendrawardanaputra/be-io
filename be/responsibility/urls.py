# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResponsibilityViewSet

router = DefaultRouter()
router.register(r'bility', ResponsibilityViewSet, basename='responsibility')

urlpatterns = [
    path('', include(router.urls)),
]
