from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from ..constants import ESTADO_CHOICES, ORIGEN_CHOICES, ORIGEN_COMPRA, ESTADO_ACTIVO

class BienPatrimonial(models.Model):

    clave_unica = models.BigAutoField(primary_key=True, verbose_name="Clave Única")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Cantidad")
    expediente = models.ForeignKey('Expediente', on_delete=models.SET_NULL, null=True, blank=True, related_name='bienes', verbose_name="N° de Expediente")
    cuenta_codigo = models.CharField(max_length=20, blank=True, verbose_name="Cuenta Código")
    nomenclatura_bienes = models.CharField(max_length=200, blank=True, verbose_name="Nomenclatura de Bienes")
    fecha_adquisicion = models.DateField(verbose_name="Fecha de Alta")
    origen = models.CharField(max_length=15, choices=ORIGEN_CHOICES, default='COMPRA', verbose_name="Origen")
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado")
    numero_serie = models.CharField(max_length=100, blank=True, verbose_name="N° de serie")
    valor_adquisicion = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True, verbose_name="Precio")
    numero_identificacion = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Número de ID")
    servicios = models.CharField(max_length=200, verbose_name="Servicios")

    class Meta:
        verbose_name = "Bien Patrimonial"
        verbose_name_plural = "Bienes Patrimoniales"
        ordering = ['clave_unica']
        indexes = [
            models.Index(fields=['clave_unica']),
            models.Index(fields=['estado']),
        ]

    def clean(self):
        super().clean()
        if self.valor_adquisicion is not None and self.valor_adquisicion < 0:
            raise ValidationError({'valor_adquisicion': 'El precio no puede ser negativo'})
        if self.fecha_adquisicion > date.today():
            raise ValidationError({'fecha_adquisicion': 'La fecha no puede ser futura'})
        if self.origen != 'COMPRA':
            self.valor_adquisicion = None