from django.urls import path
from . import views

urlpatterns = [
    path('busqueda/', views.busqueda_view, name='busqueda'),
    path('generarcotizacion/', views.generar_cotizacion_view, name='generarcotizacion'),
  
]