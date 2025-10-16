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


@admin.register(BienPatrimonial, site=custom_admin_site)
class BienPatrimonialAdmin(admin.ModelAdmin):
    list_display = [
        'clave_unica', 'nombre', 'cantidad', 'servicios', 'estado',
        'expediente', 'origen', 'valor_adquisicion'
    ]
    list_filter = ['estado', 'fecha_adquisicion', 'origen', 'expediente']
    search_fields = [
        'clave_unica', 'nombre', 'descripcion', 'numero_identificacion',
        'numero_serie', 'cuenta_codigo', 'nomenclatura_bienes', 'servicios',
        'expediente__numero_expediente'
    ]
    date_hierarchy = 'fecha_adquisicion'
    list_per_page = 25
    ordering = ('clave_unica',)
    autocomplete_fields = ['expediente']
    readonly_fields = ['clave_unica']
    fields = (
        'clave_unica',
        'nombre',
        'descripcion',
        'cantidad',
        'expediente',
        'cuenta_codigo',
        'nomenclatura_bienes',
        'fecha_adquisicion',
        'origen',
        'estado',
        'numero_serie',
        'valor_adquisicion',
        'numero_identificacion',
        'servicios',
    )

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
