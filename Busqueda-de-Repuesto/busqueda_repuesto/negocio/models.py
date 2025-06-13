from django.db import models
from django.contrib.auth.models import User

class Negocio(models.Model):
    codigo= models.CharField(max_length=5, primary_key=True)
    nombre= models.CharField(max_length=25)
    ubicacion= models.CharField(max_length=1024)
    nit=models.CharField(max_length=14)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'negocio' 
    
    def __str__(self):
        return f"{self.nombre}({self.codigo})"

