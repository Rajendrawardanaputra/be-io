# urls.py

from django.urls import path
from .views import StatusList

urlpatterns = [
    path('status/', StatusList.as_view(), name='status-list'),
    # Tambahkan path lainnya sesuai kebutuhan
]
