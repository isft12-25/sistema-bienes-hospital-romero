from django.contrib import admin

class CustomAdminSite(admin.AdminSite):
    site_header = "Gestión de Bienes Patrimoniales - Hospital Melchor Romero"
    site_title = "Sistema de Gestión"
    index_title = "Administración del Sistema"

custom_admin_site = CustomAdminSite(name='custom_admin')