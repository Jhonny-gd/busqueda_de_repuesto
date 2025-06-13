from django.urls import path
from . import views

urlpatterns = [
 
    path('buscar_vehiculo/', views.buscar_vehiculo, name='buscar_vehiculo'),
    path('consultarrepuesto/', views.consultar_view, name='consultarrepuesto'),
    path('actualizarrepuesto/', views.actualizar_view, name='actualizarrepuesto'), 
    path('agregarrepuesto/', views.agregar_view, name='agregarrepuesto')
   
]
