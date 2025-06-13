from django.db import models
from repuesto.models import Repuesto
from vehiculo.models import Vehiculo


class Cotizante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    dui = models.CharField(max_length=10)

    def _str_(self):
        return f"{self.nombre} {self.apellido}"


class VehiculoCotizacion(models.Model):
    cotizante = models.ForeignKey(Cotizante, on_delete=models.CASCADE, related_name="vehiculos")
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    transmision = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)

    def _str_(self):
        return f"{self.marca} {self.modelo} {self.anio}"


class Cotizacion(models.Model):
    cotizante = models.ForeignKey(Cotizante, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(VehiculoCotizacion, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def _str_(self):
        return f"Cotización #{self.id} - {self.cotizante}"


class DetalleRepuestoCotizado(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="detalles")
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def subtotal(self):
        return self.cantidad * self.repuesto.precio

    def _str_(self):
        return f"{self.repuesto.nombre} x {self.cantidad}"