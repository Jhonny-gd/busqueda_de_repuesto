from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('gestionar/', views.gestionar_view, name='gestionar'),
    path('gestionarrepuesto/', views.gestionar_repuesto_view, name='gestionarrepuesto'),
    path('gestionarnegocio/', views.gestionar_negocio_view, name='gestionarnegocio'),
    path('gestionarvehiculo/', views.gestionar_vehiculo_view, name='gestionarvehiculo'),
]