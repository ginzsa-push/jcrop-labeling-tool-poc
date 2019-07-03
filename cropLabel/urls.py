"""cropLabel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('init/', views.init, name='init'),
    path('createProject/', views.createProject, name='createProject'),
    path('deleteProject/<str:project_name>/', views.deleteProject, name='deleteProject'),
    path('retrieveCaptured/', views.retrieveCaptured, name='retrieveCaptured'),
    path('admin/', admin.site.urls),
    path('healthcheck/', views.healthcheck, name='healthcheck'),
    path('listImages/', views.listImages, name='listImages'),
    path('process/', views.process, name='process'),
    path('crop/', views.cropPicture, name='crop'),
    path('deleteSelected/', views.removedCropped, name='deleteSelected')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




