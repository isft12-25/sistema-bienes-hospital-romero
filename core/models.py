from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Expediente(models.Model):
    numero_expediente = models.CharField(max_length=50, unique=True)
    organismo_origen = models.CharField(max_length=120, blank=True)
    numero_compra = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        ordering = ['numero_expediente']

    def __str__(self):
        return self.numero_expediente


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

    # Origen del alta (pedido en los instructivos del profe)
    ORIGEN_CHOICES = (
        ('DONACION', 'Donación'),
        ('OMISION', 'Omisión'),
        ('TRANSFERENCIA', 'Transferencia/Traslado'),
        ('COMPRA', 'Compra'),
    )

    # Identificación principal
    numero_inventario = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()

    # Clasificación / tipo
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=100, blank=True)

    # Datos de adquisición
    fecha_adquisicion = models.DateField()
    valor_adquisicion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    proveedor = models.CharField(max_length=200, blank=True)

    # Campos adicionales solicitados por documentación (opcionales para no romper datos existentes)
    cuenta_codigo = models.CharField(max_length=20, blank=True)  # clasificación patrimonial
    origen = models.CharField(max_length=15, choices=ORIGEN_CHOICES, default='COMPRA')
    donante = models.CharField(max_length=200, blank=True)  # requerido sólo si origen=DONACION
    numero_identificacion = models.CharField(
        max_length=50,
        unique=True,
        null=True, blank=True,              # se permite nulo para migrar sin fricción
        verbose_name="Número de Identificación"
    )

    # Ubicación / estado
    ubicacion_actual = models.CharField(max_length=200)
    responsable = models.CharField(max_length=200)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='ACTIVO')

    # Vinculación con Expediente (solicitado)
    expediente = models.ForeignKey(
        Expediente,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bienes'
    )

    # Otros
    observaciones = models.TextField(blank=True)
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True)

    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Bien Patrimonial"
        verbose_name_plural = "Bienes Patrimoniales"
        ordering = ['numero_inventario']
        indexes = [
            models.Index(fields=['numero_inventario']),
            models.Index(fields=['tipo']),
            models.Index(fields=['estado']),
        ]

    def clean(self):
        """
        Validaciones de negocio mínimas:
        - Si origen es DONACION, 'donante' no puede estar vacío.
        - 'valor_adquisicion' no puede ser negativo (ya lo controla el validator).
        """
        if self.origen == 'DONACION' and not self.donante:
            raise ValidationError({'donante': 'Debe especificar el donante cuando el origen es DONACIÓN.'})

    def __str__(self):
        return f"{self.numero_inventario} - {self.nombre}"
