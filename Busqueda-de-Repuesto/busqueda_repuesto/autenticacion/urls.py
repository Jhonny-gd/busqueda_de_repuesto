from django.urls import path
from .views import login_view, logout_view, registrar_usuario


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registrar_usuario, name='registro'),
]