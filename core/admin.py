from django.contrib import admin
from .models import BienPatrimonial
from sistema_bienes.admin import custom_admin_site

@admin.register(BienPatrimonial, site=custom_admin_site)
class BienPatrimonialAdmin(admin.ModelAdmin):
    list_display = ['numero_inventario', 'nombre', 'tipo', 'ubicacion_actual', 'estado']
    list_filter = ['tipo', 'estado', 'fecha_adquisicion']
    search_fields = ['numero_inventario', 'nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']