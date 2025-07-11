"""
URL configuration for busqueda_repuesto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from autenticacion.views import logout_view
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('busqueda'), name= 'inicio'),  # Redirige a la vista de búsqueda de cotización
    path('admin/', admin.site.urls), 
    path('autenticacion/', include('autenticacion.urls')),
    path('menus/', include('menus.urls')),
    path('vehiculo/', include('vehiculo.urls')),
    path('negocio/', include('negocio.urls')),
    path('cotizacion/', include('cotizacion.urls')),
    path('repuesto/', include('repuesto.urls')),
    path('auth/', include('autenticacion.urls')),
    path('logout/', logout_view, name='logout'),  # Ruta para cerrar sesión
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)