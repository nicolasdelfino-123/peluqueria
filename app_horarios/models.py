from django.db import models


class Turno(models.Model):
    cliente = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    servicio = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.cliente} - {self.servicio} el {self.fecha} a las {self.hora}"

