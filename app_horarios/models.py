from django.db import models

class Turno(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)
    nombre_cliente = models.CharField(max_length=100, blank=True, null=True)
    apellido_cliente = models.CharField(max_length=100, blank=True, null=True)
    telefono_cliente = models.CharField(max_length=20, blank=True, null=True)
    

    def __str__(self):
        return f"{self.fecha} - {self.hora}"