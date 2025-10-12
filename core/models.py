
from datetime import date
from django.contrib.auth.models import AbstractUser 
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models



# Modelo para registrar datos básicos de un expediente (trámite/compra/origen)
class Expediente(models.Model):
    # Identificador único del expediente (texto)
    numero_expediente = models.CharField(max_length=50, unique=True)
    # Organismo desde el que proviene (opcional)
    organismo_origen = models.CharField(max_length=120, blank=True)
    # Número de compra o referencia de contratación (opcional)
    numero_compra = models.CharField(max_length=50, blank=True)

    proveedor = models.CharField(max_length=200, blank=True)

    class Meta:
        # Nombres legibles en el admin
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        # Orden por número de expediente por defecto
        ordering = ['numero_expediente']

    def __str__(self) -> str:
        # Representación en texto: muestra el número del expediente
        return str(self.numero_expediente)


# Modelo principal para representar un bien patrimonial del hospital
class Expediente(models.Model):
    numero_expediente = models.CharField(max_length=50, unique=True)
    organismo_origen = models.CharField(max_length=120, blank=True)
    numero_compra = models.CharField(max_length=50, blank=True)
    proveedor = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"
        ordering = ['numero_expediente']

    def __str__(self):
        return str(self.numero_expediente)


class BienPatrimonial(models.Model):
    # Estado / Origen
    ESTADO_CHOICES = (
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('MANTENIMIENTO', 'En mantenimiento'),
        ('BAJA', 'Dado de baja'),
    )
    ORIGEN_CHOICES = (
        ('DONACION', 'Donación'),
        ('OMISION', 'Omisión'),
        ('TRANSFERENCIA', 'Transferencia/Traslado'),
        ('COMPRA', 'Compra'),
    )

    # Identificación
    clave_unica = models.BigAutoField(primary_key=True, verbose_name="Clave Única")
    numero_identificacion = models.CharField(
        max_length=50, unique=True, null=True, blank=True, verbose_name="Número de ID"
    )
    numero_serie = models.CharField(max_length=100, blank=True, verbose_name="N° de serie")

    # Datos principales
    nombre = models.CharField(max_length=200, verbose_name="Nombre")  # (opcional quitar más adelante)
    descripcion = models.TextField(verbose_name="Descripción")
    cantidad = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name="Cantidad"
    )
    expediente = models.ForeignKey(
        'Expediente', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bienes', verbose_name="N° de Expediente"
    )
    cuenta_codigo = models.CharField(max_length=20, blank=True, verbose_name="Cuenta Código")
    nomenclatura_bienes = models.CharField(max_length=200, blank=True, verbose_name="Nomenclatura de Bienes")
    servicios = models.CharField(max_length=200, verbose_name="Servicios")

    # Situación
    origen = models.CharField(
        max_length=15, choices=ORIGEN_CHOICES, null=True, blank=True, verbose_name="Origen"
    )
    estado = models.CharField(
        max_length=50, choices=ESTADO_CHOICES, null=True, blank=True, verbose_name="Estado"
    )

    # Fechas
    fecha_adquisicion = models.DateField(null=True, blank=True, verbose_name="Fecha de Alta")
    fecha_baja = models.DateField(null=True, blank=True, verbose_name="Fecha de Baja")

    # Económico
    valor_adquisicion = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],
        null=True, blank=True, verbose_name="Precio"
    )

    # Otros
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Bien Patrimonial"
        verbose_name_plural = "Bienes Patrimoniales"
        ordering = ['clave_unica']
        indexes = [
            models.Index(fields=['clave_unica']),
            models.Index(fields=['estado']),
            models.Index(fields=['origen']),
        ]

    def __str__(self):
        return f"{self.clave_unica} - {self.descripcion[:50]}"

    def clean(self):
        super().clean()

        # Precio no puede ser negativo si viene informado
        if self.valor_adquisicion is not None and self.valor_adquisicion < 0:
            raise ValidationError({'valor_adquisicion': 'El precio no puede ser negativo'})

        # Fecha de alta no futura (si existe)
        if self.fecha_adquisicion and self.fecha_adquisicion > date.today():
            raise ValidationError({'fecha_adquisicion': 'La fecha no puede ser futura'})

        # Si origen NO es compra -> precio vacío
        if self.origen and self.origen != 'COMPRA':
            self.valor_adquisicion = None

class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado Hospital'),
    ]

    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO,
        default='empleado'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='grupos',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        related_name='usuarios_custom',
        related_query_name='usuario_custom',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permisos de usuario',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        related_name='usuarios_custom',
        related_query_name='usuario_custom',
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self) -> str:
        tipo_display = dict(self.TIPO_USUARIO).get(self.tipo_usuario, self.tipo_usuario)
        return f"{self.username} ({tipo_display})"

class Operador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Operador"
        verbose_name_plural = "Operadores"
        ordering = ['nombre_completo']

    def __str__(self) -> str:
        return str(self.nombre_completo)

    @property
    def email(self) -> str:
        """Método útil: obtiene el email del usuario sin tener que ir por usuario.email"""
        if self.usuario and hasattr(self.usuario, 'email'):
            return self.usuario.email
        return ""

    @property
    def username(self) -> str:
        """Método útil: obtiene el username sin tener que ir por usuario.username"""
        if self.usuario and hasattr(self.usuario, 'username'):
            return self.usuario.username
        return ""


