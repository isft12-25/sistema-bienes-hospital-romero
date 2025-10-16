from django.db import models

class Expediente(models.Model):
    numero_expediente = models.CharField(max_length=50, unique=True)
    organismo_origen = models.CharField(max_length=120, blank=True)
    numero_compra = models.CharField(max_length=50, blank=True)
    proveedor = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        ordering = ['numero_expediente']

    def __str__(self) -> str:
        return str(self.numero_expediente)