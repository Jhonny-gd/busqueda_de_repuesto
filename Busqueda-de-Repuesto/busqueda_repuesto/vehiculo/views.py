from django.shortcuts import render, redirect
from .models import Vehiculo
from collections import defaultdict
from .forms import VehiculoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def consultar_vehiculo_view(request):
    marca = request.GET.get('marca', '').strip()
    modelo = request.GET.get('modelo', '').strip()
    anio = request.GET.get('anio', '').strip()

    vehiculos = Vehiculo.objects.filter(usuario=request.user)  # 👈 Solo vehículos del usuario

    filtros_aplicados = marca or modelo or anio

    if filtros_aplicados:
        if marca:
            vehiculos = vehiculos.filter(marca__icontains=marca)
        if modelo:
            vehiculos = vehiculos.filter(modelo__icontains=modelo)
        if anio:
            try:
                anio = int(anio)
                if 2000 <= anio <= 2025:
                    vehiculos = vehiculos.filter(anio=anio)
                else:
                    vehiculos = []
                    messages.error(request, "Ingrese un año válido entre 2000 y 2025.")
            except ValueError:
                vehiculos = []
                messages.error(request, "Ingrese un año numérico válido.")

        if not vehiculos:
            messages.info(request, "No se encontraron vehículos con los criterios especificados.")
    else:
        vehiculos = []
        messages.error(request, "Debe ingresar al menos un criterio de búsqueda.")

    marca_modelos = defaultdict(set)
    for v in Vehiculo.objects.filter(usuario=request.user):  # 👈 Solo del usuario
        marca_modelos[v.marca].add(v.modelo)
    marca_modelos = {marca: list(modelos) for marca, modelos in marca_modelos.items()}

    marcas = Vehiculo.objects.filter(usuario=request.user).values_list('marca', flat=True).distinct()
    modelos = Vehiculo.objects.filter(usuario=request.user).values_list('modelo', flat=True).distinct()

    return render(request, 'vehiculo/consultar-vehiculo.html', {
        'vehiculos': vehiculos,
        'marcas': marcas,
        'modelos': modelos,
        'marca_modelos': marca_modelos,
    })


@login_required
def agregar_vehiculo_view(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST or None, user=request.user)  # 👈 Pasar el usuario logueado al formulario
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.usuario = request.user  # 👈 Asignar usuario logueado
            vehiculo.save()
            messages.success(request, 'Vehículo agregado exitosamente.')
            form = VehiculoForm(user=request.user)  # 👈 Reiniciar el formulario
    else:
        form = VehiculoForm()

    return render(request, 'vehiculo/agregar-vehiculo.html', {'form': form})


@login_required
def eliminar_vehiculo_view(request):
    desde_eliminacion = request.session.pop('vehiculo_eliminado', False)

    marca = request.GET.get('marca', '').strip()
    modelo = request.GET.get('modelo', '').strip()
    anio = request.GET.get('anio', '').strip()

    vehiculos = Vehiculo.objects.filter(usuario=request.user)  # 👈 Solo vehículos del usuario

    filtros_aplicados = marca or modelo or anio

    if filtros_aplicados:
        if marca:
            vehiculos = vehiculos.filter(marca__icontains=marca)
        if modelo:
            vehiculos = vehiculos.filter(modelo__icontains=modelo)
        if anio:
            try:
                anio = int(anio)
                if 2000 <= anio <= 2025:
                    vehiculos = vehiculos.filter(anio=anio)
                else:
                    vehiculos = Vehiculo.objects.none()
                    messages.error(request, "Ingrese un año válido entre 2000 y 2025.")
            except ValueError:
                vehiculos = Vehiculo.objects.none()
                messages.error(request, "Ingrese un año numérico válido.")

        if not vehiculos.exists():
            messages.info(request, "No se encontraron vehículos con los criterios especificados.")
    else:
        vehiculos = Vehiculo.objects.none()
        if not desde_eliminacion:
            messages.error(request, "Debe ingresar al menos un criterio de búsqueda.")

    if request.method == 'POST':
        id_auto = request.POST.get('radio_seleccionar')
        if id_auto:
            try:
                vehiculo = Vehiculo.objects.get(id_auto=id_auto, usuario=request.user)  # 👈 Asegurar que sea del usuario
                vehiculo.delete()
                messages.success(request, 'Vehículo eliminado exitosamente.')
                request.session['vehiculo_eliminado'] = True
                return redirect('eliminarvehiculo')
            except Vehiculo.DoesNotExist:
                messages.error(request, 'El vehículo no existe o no pertenece a este usuario.')
        else:
            messages.error(request, 'Debe seleccionar un vehículo para eliminar.')

    marca_modelos = defaultdict(set)
    for v in Vehiculo.objects.filter(usuario=request.user):  # 👈 Solo del usuario
        marca_modelos[v.marca].add(v.modelo)
    marca_modelos = {marca: list(modelos) for marca, modelos in marca_modelos.items()}

    marcas = Vehiculo.objects.filter(usuario=request.user).values_list('marca', flat=True).distinct()
    modelos = Vehiculo.objects.filter(usuario=request.user).values_list('modelo', flat=True).distinct()

    return render(request, 'vehiculo/eliminar-vehiculo.html', {
        'vehiculos': vehiculos,
        'marcas': marcas,
        'modelos': modelos,
        'marca_modelos': marca_modelos,
    })
