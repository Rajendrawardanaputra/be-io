# urls.py
from django.urls import path
from .views import OverallStatusView

urlpatterns = [
    # ... path lainnya ...
    path('overallstatus/', OverallStatusView.as_view(), name='overall_status'),
]
