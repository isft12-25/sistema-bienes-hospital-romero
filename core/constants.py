"""
Constantes del proyecto Sistema de Bienes Patrimoniales
"""

# Estados de bienes patrimoniales
ESTADO_ACTIVO = 'ACTIVO'
ESTADO_INACTIVO = 'INACTIVO'
ESTADO_MANTENIMIENTO = 'MANTENIMIENTO'
ESTADO_BAJA = 'BAJA'

ESTADO_CHOICES = (
    (ESTADO_ACTIVO, 'Activo'),
    (ESTADO_INACTIVO, 'Inactivo'),
    (ESTADO_MANTENIMIENTO, 'En mantenimiento'),
    (ESTADO_BAJA, 'Dado de baja'),
)

# Orígenes de bienes
ORIGEN_DONACION = 'DONACION'
ORIGEN_OMISION = 'OMISION'
ORIGEN_TRANSFERENCIA = 'TRANSFERENCIA'
ORIGEN_COMPRA = 'COMPRA'

ORIGEN_CHOICES = (
    (ORIGEN_DONACION, 'Donación'),
    (ORIGEN_OMISION, 'Omisión'),
    (ORIGEN_TRANSFERENCIA, 'Transferencia/Traslado'),
    (ORIGEN_COMPRA, 'Compra'),
)
