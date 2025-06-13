from django.db import models

class Usuario(models.Model):
    dui = models.CharField(max_length=9, unique=True, primary_key=True)  # Ahora es primary key
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    email = models.CharField(unique=True, max_length=25)
    clave = models.CharField(max_length=15)  # Guarda claves cifradas preferiblemente
    telefono = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'usuario'
