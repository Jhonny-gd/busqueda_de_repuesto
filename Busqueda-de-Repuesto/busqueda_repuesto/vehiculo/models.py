from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vehiculo(models.Model):
   id_auto = models.CharField(primary_key=True, max_length=10)
   
   marca = models.CharField(max_length=100)
   modelo = models.CharField(max_length=100)
   anio = models.IntegerField()
   transmision = models.CharField(max_length=50)
   tipo = models.CharField(max_length=50)
   usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Relación con el modelo User de Django
   class Meta:
        db_table = 'vehiculo'  # Este es el nombre exacto de la tabla en PostgreSQL
   def __str__(self):
        return f"{self.marca} {self.modelo} {self.anio}"
    