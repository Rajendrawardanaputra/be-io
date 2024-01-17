"""
URL configuration for be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/', include('detailmanpower.urls')),
    path('api/', include('karyawan.urls')),
    path('api/', include('projectinternal.urls')),
    path('api/', include('projectcharter.urls')),
    path('api/', include('description.urls')),
    path('api/', include('deliverable.urls')),
    path('api/', include('detailmilostones.urls')),
    path('api/', include('milostones.urls')),
    path('api/', include('detail_responsibilities.urls')),
    path('api/', include('responsibility.urls')),
    path('api/', include('supporting.urls')),
    path('api/', include('detailsupporting.urls')),
    path('api/', include('approvedBy.urls')),
    path('api/', include('users.urls')),
    path('api/', include('timeline.urls')),
    
]
