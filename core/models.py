

from django.db import models
from django.contrib.auth.models import User

class BienPatrimonial(models.Model):
    ESTADO_CHOICES = (
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('MANTENIMIENTO', 'En mantenimiento'),
        ('BAJA', 'Dado de baja'),
    )
    
    TIPO_CHOICES = (
        ('EQUIPO_MEDICO', 'Equipo Médico'),
        ('INFORMATICA', 'Equipo Informático'),
        ('MOBILIARIO', 'Mobiliario'),
        ('VEHICULO', 'Vehículo'),
        ('OTRO', 'Otro'),
    )
    
    numero_inventario = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=100, blank=True)
    
    fecha_adquisicion = models.DateField()
    valor_adquisicion = models.DecimalField(max_digits=12, decimal_places=2)
    proveedor = models.CharField(max_length=200, blank=True)
    
    ubicacion_actual = models.CharField(max_length=200)
    responsable = models.CharField(max_length=200)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='ACTIVO')
    
    observaciones = models.TextField(blank=True)
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Bien Patrimonial"
        verbose_name_plural = "Bienes Patrimoniales"
        ordering = ['numero_inventario']

    def __str__(self):
        return f"{self.numero_inventario} - {self.nombre}"