from django.urls import path
from .views import DetailTimelineListCreateAPIView, DetailTimelineDetailAPIView, DetailTimelinePublicListCreateAPIView, DetailTimelinePublicDetailAPIView

urlpatterns = [
    path('timeline/', DetailTimelineListCreateAPIView.as_view(), name='detail-timeline-list-create'),
    path('timeline/<int:pk>/', DetailTimelineDetailAPIView.as_view(), name='detail-timeline-detail'),
    path('timelinemobile/', DetailTimelinePublicListCreateAPIView.as_view(), name='detail-timeline-detail'),
    path('timelinemobile/<int:pk>/', DetailTimelinePublicDetailAPIView.as_view(), name='detail-timeline-detail'),
    # path('timeline/login/', get_user_info, name='get_user_info'),
]
