from django.urls import path
from . import views

urlpatterns = [
    path('actualizarnegocio/', views.actualizar_negocio_view, name='actualizarnegocio'),
    path('agregarnegocio/', views.agregar_negocio_view, name='agregarnegocio'),
    path('eliminarnegocio/', views.eliminar_negocio_view, name='eliminarnegocio'),
    path('consultarnegocio/', views.consultar_negocio_view, name='consultarnegocio'),

   
]