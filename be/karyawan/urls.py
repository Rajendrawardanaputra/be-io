from django.urls import path
from .views import ActivityLogListView

urlpatterns = [
    # ... your other URL patterns ...
    path('activitylog/', ActivityLogListView.as_view(), name='activitylog-list'),
]
