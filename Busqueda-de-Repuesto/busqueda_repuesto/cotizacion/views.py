from django.shortcuts import render, redirect
from .forms import CotizanteForm
from .models import Cotizante, Cotizacion, DetalleRepuestoCotizado
from repuesto.models import Repuesto
from vehiculo.models import Vehiculo
from django.db.models import Q

def busqueda_view(request):
    cotizante_id = request.session.get('cotizante_id')
    cotizante_form = CotizanteForm()
    repuestos = []
    mensaje = None

    # Filtros únicos para selects
    marcas = Vehiculo.objects.values_list('marca', flat=True).distinct()
    modelos = Vehiculo.objects.values_list('modelo', flat=True).distinct()
    anios = Vehiculo.objects.values_list('anio', flat=True).distinct()
    transmisiones = Vehiculo.objects.values_list('transmision', flat=True).distinct()
    tipos = Vehiculo.objects.values_list('tipo', flat=True).distinct()

    if request.method == 'POST':
        if 'ingresar_cotizante' in request.POST:
            cotizante_form = CotizanteForm(request.POST)
            if cotizante_form.is_valid():
                cotizante = cotizante_form.save()
                request.session['cotizante_id'] = cotizante.id
            else:
                mensaje = "Por favor, complete todos los campos del cotizante correctamente."

        elif 'buscar_repuestos' in request.POST:
            nombre = request.POST.get('nombre_repuesto', '')
            categoria = request.POST.get('categoria', '')
            estado = request.POST.get('estado', '')
            orden = request.POST.get('orden', '')

            # Filtros del vehículo
            marca = request.POST.get('marca')
            modelo = request.POST.get('modelo')
            anio = request.POST.get('anio')
            transmision = request.POST.get('transmision')
            tipo = request.POST.get('tipo')

            repuestos = Repuesto.objects.filter(nombre__icontains=nombre)

            if categoria:
                repuestos = repuestos.filter(categoria=categoria)
            if estado:
                repuestos = repuestos.filter(estado=estado)

            # Filtrado por compatibilidad
            if marca or modelo or anio or transmision or tipo:
                repuestos = repuestos.filter(
                    compatibilidad__marca__icontains=marca,
                    compatibilidad__modelo__icontains=modelo,
                    compatibilidad__anio__icontains=anio,
                    compatibilidad__transmision__icontains=transmision,
                    compatibilidad__tipo__icontains=tipo,
                ).distinct()

            if orden == 'asc':
                repuestos = repuestos.order_by('precio')
            elif orden == 'desc':
                repuestos = repuestos.order_by('-precio')

            if not repuestos:
                mensaje = "No se encontraron repuestos."

        elif 'agregar_repuesto' in request.POST:
            repuesto_id = request.POST.get('agregar_repuesto')
           # cantidad = int(request.POST.get(f'cantidad_{repuesto_id}', 1)) # Valor por defecto de 1
            cantidad_key = f'cantidad_{repuesto_id}'
            cantidad=int(request.POST.get(cantidad_key, 1)) 

            if repuesto_id and cantidad:
                carrito = request.session.get('carrito', [])
                carrito.append({'repuesto_id': repuesto_id, 'cantidad': cantidad})
                request.session['carrito'] = carrito

        elif 'generar_cotizacion' in request.POST:
            if cotizante_id:
                cotizante = Cotizante.objects.get(id=cotizante_id)
                cotizacion = Cotizacion.objects.create(cotizante=cotizante, vehiculo=None)

                carrito = request.session.get('carrito', [])
                total = 0
                for item in carrito:
                    repuesto = Repuesto.objects.get(id=item['repuesto_id'])
                    cantidad = item['cantidad']
                    subtotal = repuesto.precio * cantidad
                    total += subtotal
                    DetalleRepuestoCotizado.objects.create(
                        cotizacion=cotizacion,
                        repuesto=repuesto,
                        cantidad=cantidad
                    )

                cotizacion.total = total
                cotizacion.save()
                request.session.flush()
                return redirect('generarcotizacion')
            else:
                mensaje = "Debe ingresar un cotizante antes de generar la cotización."

    # Si ya se había guardado el cotizante, volver a mostrar sus datos
    if cotizante_id:
        try:
            cotizante = Cotizante.objects.get(id=cotizante_id)
            cotizante_form = CotizanteForm(instance=cotizante)
        except Cotizante.DoesNotExist:
            cotizante_form = CotizanteForm()
            mensaje = "Cotizante no encontrado."

    context = {
        'cotizante_form': cotizante_form,
        'repuestos': repuestos,
        'mensaje': mensaje,
        'carrito': request.session.get('carrito', []),
        'vehiculo_seleccionado': False,
        'marcas': marcas,
        'modelos': modelos,
        'anios': anios,
        'transmisiones': transmisiones,
        'tipos': tipos,
    }

    return render(request, 'cotizacion/busqueda.html', context)


def generar_cotizacion_view(request):
    cotizacion = Cotizacion.objects.latest('id')
    return render(request, 'cotizacion/generar-cotizacion.html', {'cotizacion': cotizacion})