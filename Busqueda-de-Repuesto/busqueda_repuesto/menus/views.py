from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Ajusta según tu URL de login

def gestionar_view(request):
    return render(request, 'menus/gestionar.html')
def gestionar_repuesto_view(request):
    return render(request, 'menus/gestionar-repuesto.html')

def gestionar_negocio_view(request):
    return render(request, 'menus/gestionar-negocio.html')   
   
def gestionar_vehiculo_view(request):
    return render(request, 'menus/gestionar-vehiculo.html')

