from django.contrib import admin
from .models import BienPatrimonial, Expediente
from sistema_bienes.admin import custom_admin_site


@admin.register(Expediente, site=custom_admin_site)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ['numero_expediente', 'organismo_origen', 'numero_compra']
    search_fields = ['numero_expediente', 'organismo_origen', 'numero_compra']
    ordering = ['numero_expediente']


class BienInline(admin.TabularInline):
    """
    Inline para ver (opcionalmente) bienes dentro de un expediente desde el admin de Expediente.
    Podés comentarlo si no lo querés usar.
    """
    model = BienPatrimonial
    extra = 0
    fields = ['numero_inventario', 'nombre', 'tipo', 'estado', 'ubicacion_actual']
    readonly_fields = ['numero_inventario', 'nombre', 'tipo', 'estado', 'ubicacion_actual']
    can_delete = False

@admin.register(BienPatrimonial, site=custom_admin_site)
class BienPatrimonialAdmin(admin.ModelAdmin):
    list_display = [
        'numero_inventario', 'nombre', 'tipo', 'ubicacion_actual', 'estado',
        'expediente', 'origen', 'valor_adquisicion'
    ]
    list_filter = ['tipo', 'estado', 'fecha_adquisicion', 'origen', 'expediente']
    search_fields = [
        'numero_inventario', 'nombre', 'descripcion',
        'numero_identificacion', 'ubicacion_actual',
        'expediente__numero_expediente'
    ]
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_adquisicion'
    list_per_page = 25
    ordering = ('numero_inventario',)
    autocomplete_fields = ['expediente']

    def save_model(self, request, obj, form, change):
        """
        Forzamos validaciones del modelo (clean/validators) al guardar desde el admin.
        """
        obj.full_clean()
        super().save_model(request, obj, form, change)
