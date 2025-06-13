from django.urls import path
from . import views

urlpatterns = [
    path('consultarvehiculo/', views.consultar_vehiculo_view, name='consultarvehiculo'),
    path('agregarvehiculo/', views.agregar_vehiculo_view, name='agregarvehiculo'),
    path('eliminarvehiculo/', views.eliminar_vehiculo_view, name='eliminarvehiculo'),
    
]