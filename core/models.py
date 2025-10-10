from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



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

    def __str__(self):
        # Representación en texto: muestra el número del expediente
        return self.numero_expediente


# Modelo principal para representar un bien patrimonial del hospital
class BienPatrimonial(models.Model):
    # Estados posibles del bien para control de ciclo de vida
    ESTADO_CHOICES = (
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('MANTENIMIENTO', 'En mantenimiento'),
        ('BAJA', 'Dado de baja'),
    )

    # Origen del bien (cómo ingresó al patrimonio)
    ORIGEN_CHOICES = (
        ('DONACION', 'Donación'),
        ('OMISION', 'Omisión'),
        ('TRANSFERENCIA', 'Transferencia/Traslado'),
        ('COMPRA', 'Compra'),
    )

    # Identificador interno único del inventario (placa/etiqueta)
    numero_inventario = models.CharField(max_length=50, unique=True)
    # Nombre corto del bien
    nombre = models.CharField(max_length=200)
    # Descripción detallada
    descripcion = models.TextField()
    # Tipo/clasificación del bien (usa TIPO_CHOICES)
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    # Número de serie de fábrica (opcional)
    numero_serie = models.CharField(max_length=100, blank=True)

    # Datos de adquisición
    fecha_adquisicion = models.DateField()
    # Valor de compra/donación; no puede ser negativo
    valor_adquisicion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    # Proveedor (si aplica)
    proveedor = models.CharField(max_length=200, blank=True)

    # Información contable y de origen
    cuenta_codigo = models.CharField(max_length=20, blank=True)
    # Origen del bien (por defecto: COMPRA)
    origen = models.CharField(max_length=15, choices=ORIGEN_CHOICES, default='COMPRA')
    # Donante (solo relevante si origen es DONACION)
    donante = models.CharField(max_length=200, blank=True)
    # Identificación adicional única (ej. código patrimonial externo)
    numero_identificacion = models.CharField(
        max_length=50,
        unique=True,
        null=True, blank=True,
        verbose_name="Número de Identificación"
    )

    # Ubicación física actual (servicio/dependencia) y responsable
    servicios = models.CharField(max_length=200)
    responsable = models.CharField(max_length=200)
    # Estado actual del bien (usa ESTADO_CHOICES; por defecto ACTIVO)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='ACTIVO')

    # Relación opcional con un expediente; si se borra el expediente, queda en NULL
    expediente = models.ForeignKey(
        Expediente,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bienes'  # permite expediente.bienes.all()
    )

    # Observaciones y mantenimiento preventivo/correctivo
    observaciones = models.TextField(blank=True)
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True)

    # Metadatos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # se setea al crear
    fecha_actualizacion = models.DateTimeField(auto_now=True)  # se actualiza en cada save
    # Usuario que creó el registro; si se borra el usuario, queda en NULL
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        # Nombres legibles y orden por número de inventario
        verbose_name = "Bien Patrimonial"
        verbose_name_plural = "Bienes Patrimoniales"
        ordering = ['numero_inventario']
        # Índices para acelerar búsquedas frecuentes
        indexes = [
            models.Index(fields=['numero_inventario']),
            models.Index(fields=['estado']),
        ]

    def clean(self):
        """
        Validaciones de negocio mínimas que se ejecutan antes de guardar (full_clean):
        - Si el origen es DONACION, el campo 'donante' es obligatorio.
        """
        if self.origen == 'DONACION' and not self.donante:
            # Se asocia el error al campo 'donante' para que el admin/form lo muestre ahí
            raise ValidationError({'donante': 'Debe especificar el donante cuando el origen es DONACIÓN.'})

    def __str__(self):
        # Representación en texto: "NroInventario - Nombre"
        return f"{self.numero_inventario} - {self.nombre}"

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
    
    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"

