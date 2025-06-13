from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistroUsuarioForm

def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente. Ya puedes iniciar sesión.")
            return redirect('login')  # Usa el nombre de tu URL de login
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = RegistroUsuarioForm()

    return render(request, "autenticacion/registro.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Inicia sesión
           
            return redirect('gestionar')  # Aquí pones la url a donde quieres enviar tras login
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = AuthenticationForm()

    return render(request, 'autenticacion/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')  # Cambia si quieres que vaya a otra página
