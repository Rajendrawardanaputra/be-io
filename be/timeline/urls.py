from django.urls import path
from .views import DetailTimelineListCreateAPIView, DetailTimelineDetailAPIView

urlpatterns = [
    path('timeline/', DetailTimelineListCreateAPIView.as_view(), name='detail-timeline-list-create'),
    path('timeline/<int:pk>/', DetailTimelineDetailAPIView.as_view(), name='detail-timeline-detail'),
    # path('timeline/login/', get_user_info, name='get_user_info'),
]
