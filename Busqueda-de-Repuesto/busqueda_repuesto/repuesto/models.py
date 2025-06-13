from django.db import models
from vehiculo.models import Vehiculo  # Importas el modelo original de la otra app
from negocio.models import Negocio  # Importas el modelo de negocio para la relación
from django.contrib.auth.models import User  # Importas el modelo de usuario para la relación

class Repuesto(models.Model):
    num_parte= models.CharField(max_length=15, unique=True)  # Número de parte único para el repuesto
    nombre = models.CharField(max_length=100)
    
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=50)
    categoria = models.CharField(max_length=45)
    estado = models.CharField(max_length=10, choices=[
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado')])
    foto = models.ImageField(upload_to='repuestos/', null=True, blank=True)  # Campo para la foto del repuesto

    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE)  # Relación con el negocio al que pertenece el repuesto
    compatibilidad = models.ManyToManyField(Vehiculo, related_name='repuestos_compatibles', blank=True)  # Relación con los vehículos compatibles
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Relación con el usuario que creó el repuesto

    cantidad = models.IntegerField()  # Cantidad disponible del repuesto


    class Meta:
        db_table = 'repuesto'  # Nombre de la tabla para repuestos

    def __str__(self):
        return f"{self.nombre} para {self.vehiculo}"