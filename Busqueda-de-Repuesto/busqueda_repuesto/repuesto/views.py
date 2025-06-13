from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import RepuestoForm
from .models import Repuesto
from vehiculo.models import Vehiculo
from negocio.models import Negocio

@login_required
def agregar_view(request):
    vehiculos = Vehiculo.objects.filter(usuario=request.user)
    negocios = Negocio.objects.filter(usuario=request.user)

    if request.method == 'POST':
        form = RepuestoForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            print("compatibilidad ", request.POST.getlist('compatibilidad'))  # Depuración opcional
           
            num_parte = form.cleaned_data.get('num_parte')
            if Repuesto.objects.filter(num_parte=num_parte).exists():
                messages.error(request, f"Ya existe un repuesto con el número de parte '{num_parte}'.")
            else:
                repuesto = form.save(commit=False)
                repuesto.usuario = request.user
                repuesto.save()
                form.save_m2m()
                messages.success(request, "Repuesto agregado correctamente.")
                return redirect('agregarrepuesto')
        else:
            messages.error(request, "Corrige los errores del formulario.")
            print("Errores del formulario:", form.errors)

    else:
        form = RepuestoForm(user=request.user)

    return render(request, 'repuesto/agregar.html', {
        'form': form,
        'vehiculos': vehiculos,
        'negocios': negocios
    })
@login_required
def consultar_view(request):
    repuestos = Repuesto.objects.filter(usuario=request.user)
    negocios = Negocio.objects.filter(usuario=request.user)

    # Filtros
    nombre = request.GET.get('nombre-repuesto', '')
    categoria = request.GET.get('categoria', '')
    sucursal_id = request.GET.get('sucursal', '')

    if nombre:
        repuestos = repuestos.filter(nombre__icontains=nombre)
    if categoria:
        repuestos = repuestos.filter(categoria=categoria)
    if sucursal_id:
        repuestos = repuestos.filter(negocio_id=sucursal_id)

    return render(request, 'repuesto/consultar.html', {
        'repuestos': repuestos,
        'negocios': negocios,
    })

@login_required
def buscar_vehiculo(request):
    modelo = request.GET.get('modelo_buscar', '')
    vehiculos = Vehiculo.objects.filter(modelo__icontains=modelo, usuario=request.user)

    data = [{
        'id_auto': v.id_auto,
        'marca': v.marca,
        'modelo': v.modelo,
        'anio': v.anio,
        'tipo': v.tipo,
        'transmision': v.transmision
    } for v in vehiculos]

    return JsonResponse(data, safe=False)

@login_required
def actualizar_view(request):
    repuestos = None
    repuesto = None
    form = None

    categorias = Repuesto.objects.values_list('categoria', flat=True).distinct()
    negocios = Negocio.objects.filter(usuario=request.user)
    vehiculos = Vehiculo.objects.filter(usuario=request.user)

    if request.method == 'GET':
        nombre = request.GET.get('nombre-repuesto', '')
        categoria = request.GET.get('categoria_buscar', '')
        num_parte = request.GET.get('num_parte')

        # Si hay búsqueda, filtra los repuestos
        if nombre or categoria:
            repuestos = Repuesto.objects.filter(usuario=request.user)
            if nombre:
                repuestos = repuestos.filter(nombre__icontains=nombre)
            if categoria:
                repuestos = repuestos.filter(categoria=categoria)

        # Si seleccionas un repuesto para editar
        if num_parte:
            repuesto = get_object_or_404(Repuesto, num_parte=num_parte, usuario=request.user)
            form = RepuestoForm(instance=repuesto, user=request.user)
            vehiculos_compatibles = repuesto.compatibilidad.all()
        else:
            form = RepuestoForm(user=request.user)
            vehiculos_compatibles = []

    elif request.method == 'POST':
        num_parte = request.POST.get('num_parte')
        repuesto = get_object_or_404(Repuesto, num_parte=num_parte, usuario=request.user)
        form = RepuestoForm(request.POST, request.FILES, instance=repuesto, user=request.user)

        if form.is_valid():
            repuesto_obj = form.save(commit=False)
            # Verifica si el número de parte ya existe para otro repuesto
            repuesto_obj.usuario = request.user # Asegúrate de asignar el usuario actual
            repuesto_obj.save()
            form.save_m2m() # Guarda las relaciones ManyToMany
           
            messages.success(request, "Repuesto actualizado correctamente.")
            return redirect('actualizarrepuesto')
        else:
            print(form.errors)  # <-- Mira la consola para ver si hay errores
            messages.error(request, "Error al actualizar el repuesto.")

    return render(request, 'repuesto/actualizar.html', {
        'form': form,
        'vehiculos_compatibles': vehiculos_compatibles,
        'categorias': categorias,
        'repuestos': repuestos,
        'repuesto': repuesto,
        'form': form,
        'vehiculos': vehiculos,
        'negocios': negocios,
    })