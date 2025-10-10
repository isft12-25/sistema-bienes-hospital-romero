from django.contrib import admin
from .models import BienPatrimonial, Expediente
from sistema_bienes.admin import custom_admin_site  # Sitio de admin personalizado (en lugar del admin por defecto)


# Registro del modelo Expediente en el admin personalizado
@admin.register(Expediente, site=custom_admin_site)
class ExpedienteAdmin(admin.ModelAdmin):
    # Columnas que se muestran en la lista de expedientes
    list_display = ['numero_expediente', 'organismo_origen', 'numero_compra','proveedor']
    # Campos por los que se puede buscar (incluye coincidencias parciales)
    search_fields = ['numero_expediente', 'organismo_origen', 'numero_compra','proveedor']
    # Orden por defecto en la vista de lista
    ordering = ['numero_expediente']


# Inline para visualizar (solo lectura) bienes vinculados a un expediente
class BienInline(admin.TabularInline):
    """Inline para ver bienes dentro de un expediente desde el admin de Expediente."""
    model = BienPatrimonial
    extra = 0  # No mostrar filas vacías adicionales
    # Campos visibles en la tabla inline
    fields = ['numero_inventario', 'nombre', 'tipo', 'estado', 'servicios']
    # Todos los campos solo lectura (visualización sin edición)
    readonly_fields = ['numero_inventario', 'nombre', 'tipo', 'estado', 'servicios']
    can_delete = False  # Evita borrar bienes desde el inline

# Nota: si querés habilitar el inline en la vista de Expediente, agregá:
# ExpedienteAdmin.inlines = [BienInline]


# Registro del modelo BienPatrimonial en el admin personalizado
@admin.register(BienPatrimonial, site=custom_admin_site)
class BienPatrimonialAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista de bienes para una vista rápida y útil
    list_display = [
        'numero_inventario', 'nombre', 'servicios', 'estado',
        'expediente', 'origen', 'valor_adquisicion'
    ]
    # Filtros laterales para segmentar resultados
    list_filter = [ 'estado', 'fecha_adquisicion', 'origen', 'expediente']
    # Campos y relaciones por los que se puede buscar
    # Ojo con 'expediente__numero_expediente': uso de doble guion bajo para buscar por campo de FK
    search_fields = [
        'numero_inventario', 'nombre', 'descripcion',
        'numero_identificacion', 'servicios',
        'expediente__numero_expediente'
    ]
    # Campos que no se pueden editar manualmente (se llenan automáticamente)
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    # Navegación por fecha en la parte superior usando 'fecha_adquisicion'
    date_hierarchy = 'fecha_adquisicion'
    # Paginación en la lista
    list_per_page = 25
    # Orden por defecto
    ordering = ('numero_inventario',)
    # Autocompletar el campo expediente (útil si hay muchos expedientes)
    autocomplete_fields = ['expediente']

    def save_model(self, request, obj, form, change):
        """
        Al guardar desde el admin, forzamos las validaciones del modelo:
        - Ejecuta clean() y los validators antes de hacer el save.
        - Si hay errores, se muestran en el formulario del admin.
        """
        obj.full_clean()  # dispara clean() + validators de fields
        super().save_model(request, obj, form, change)
