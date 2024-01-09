from django.urls import path
from .views import login

urlpatterns = [
    # ... path lainnya ...
    path('auth/', login, name='login'),
]
