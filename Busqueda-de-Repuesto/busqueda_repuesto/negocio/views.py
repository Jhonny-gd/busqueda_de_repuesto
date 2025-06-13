from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Negocio
from .forms import NegocioForm
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages

@login_required
def agregar_negocio_view(request):
    form = NegocioForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            negocio = form.save(commit=False)
            negocio.usuario = request.user
            if Negocio.objects.filter(codigo=negocio.codigo, usuario=request.user).exists():
                messages.warning(request, "Ya existe un negocio con ese código")
            elif len(negocio.nit) != 14:
                messages.warning(request, "El NIT debe contener 14 dígitos")
            elif Negocio.objects.filter(nit=negocio.nit, usuario=request.user).exists():
                messages.warning(request, "Ya existe un negocio con ese NIT")
            else:
                negocio.save()
                messages.success(request, "Negocio agregado exitosamente")
                return redirect('agregarnegocio')
    return render(request, 'negocio/agregar-negocio.html', {'form': form})

@login_required
def actualizar_negocio_view(request):
    resultados = []
    texto = ''
    if request.method == 'GET':
        texto = request.GET.get('txtBuscarNegocio', '')
        if texto:
            resultados = Negocio.objects.filter(nombre__icontains=texto, usuario=request.user)
    elif request.method == 'POST':
        codigo = request.POST.get('txtCodigoNegocio')
        nombre = request.POST.get('txtNombreNegocio')
        nit = request.POST.get('txtNitNegocio')
        ubicacion = request.POST.get('txtUbicacionNegocio')
        try:
            negocio = Negocio.objects.get(codigo=codigo, usuario=request.user)
            negocio.nombre = nombre
            negocio.ubicacion = ubicacion
            # negocio.nit = nit  # Si quieres permitir cambiar el NIT
            negocio.save()
            messages.success(request, "Negocio actualizado correctamente.")
            texto = ''  # <-- Limpia el campo de búsqueda aquí
        except Negocio.DoesNotExist:
            messages.error(request, "No se encontró el negocio para actualizar.")
            texto = nombre  # Solo en caso de error, deja el texto
        resultados = Negocio.objects.filter(nombre__icontains=texto, usuario=request.user)

    return render(request, 'negocio/actualizar-negocio.html', {
        'resultados': resultados,
        'texto': texto,
    })

@login_required
def eliminar_negocio_view(request):
    texto = request.GET.get("txtBuscarNegocio", "")
    resultados = Negocio.objects.filter(usuario=request.user)

    if texto:
        resultados = resultados.filter(nombre__icontains=texto)

    if request.method == "POST" and "btnEliminar" in request.POST:
        codigo = request.POST.get("codigoEliminar")
        try:
            negocio = get_object_or_404(Negocio, codigo=codigo, usuario=request.user)
            negocio.delete()
            messages.success(request, "Negocio eliminado correctamente")
        except IntegrityError:
            messages.error(request, "El negocio no se puede eliminar porque está relacionado con otros registros")
        return redirect('eliminarnegocio')

    return render(request, "negocio/eliminar-negocio.html", {
        "resultados": resultados,
        "texto": texto
    })

@login_required
def consultar_negocio_view(request):
    texto = request.GET.get('txtNombreNegocio', '').strip()
    resultados = Negocio.objects.filter(usuario=request.user)

    if texto:
        resultados = resultados.filter(nombre__icontains=texto)

    return render(request, 'negocio/consultar-negocio.html', {
        'resultados': resultados,
        'texto': texto
    })