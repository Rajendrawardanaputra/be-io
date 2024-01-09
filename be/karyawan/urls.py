# urls.py

from django.urls import path
from .views import (
    tambah_internal_order,
    lihat_project_internal,
    update_project_internal,
    hapus_project_internal,
)

urlpatterns = [
    path('tambah_internal_order/', tambah_internal_order, name='tambah_internal_order'),
    path('lihat_project_internal/<int:id>/', lihat_project_internal, name='lihat_project_internal'),
    path('update_project_internal/<int:id>/', update_project_internal, name='update_project_internal'),
    path('hapus_project_internal/<int:id>/', hapus_project_internal, name='hapus_project_internal'),
    # Tambahkan path lain sesuai kebutuhan
]
