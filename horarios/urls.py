"""
URL configuration for horarios project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# horarios/urls.py
from django.contrib import admin
from django.urls import path
from app_horarios import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_views.index, name='index'),
    path('crear_turno/', app_views.crear_turno, name='crear_turno'),
    path('editar_turno/<int:turno_id>/', app_views.editar_turno, name='editar_turno'),
    # Otras URLs según sea necesario
]
