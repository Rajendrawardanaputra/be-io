# urls.py
from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, login_view, get_user_info

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('login/', login_view, name='login'),
    path('user/login/', get_user_info, name='get_user_info'),
]
