
from django.http import HttpResponse
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    

    # Admin / Operadores
    path('home_admin/', views.home_admin, name='home_admin'),
    path('alta_operadores/', views.alta_operadores, name='alta_operadores'),
    path('operadores.html', views.operadores, name='operadores'),
    # Vistas varias (si las usás como páginas sueltas)
    path("base/", views.base, name="base"),
    path("reportes/", views.reportes_view, name="reportes"),
    path("alta-operadores/", views.alta_operadores, name="alta_operadores"),

    # ============ BIENES ============
    # Lista general
    path("lista-bienes/", views.lista_bienes, name="lista_bienes"),
    # Carga masiva
    path("carga-masiva/", views.carga_masiva_bienes, name="carga_masiva"),
    # CRUD / acciones
    path("bienes/<int:pk>/editar/", views.editar_bien, name="editar_bien"),
    path("bienes/<int:pk>/eliminar/", views.eliminar_bien, name="eliminar_bien"),  # elimina físico (no baja)
    path("bienes/eliminar-seleccionados/", views.eliminar_bienes_seleccionados, name="eliminar_bienes_seleccionados"),

    # Bajas
    path("bienes/bajas/", views.lista_baja_bienes, name="lista_baja_bienes"),
    path("bienes/<int:pk>/dar-baja/", views.dar_baja_bien, name="dar_baja_bien"),
    path("bienes/<int:pk>/restablecer/", views.restablecer_bien, name="restablecer_bien"),
    path("bienes/<int:pk>/eliminar-definitivo/", views.eliminar_bien_definitivo, name="eliminar_bien_definitivo"),

    # (Opcional) plantillas “legacy” si aún las navegás directo
    path("bienes.html", views.bienes, name="bienes"),
    path("bien_confirm_delete/", views.bien_confirm_delete, name="bien_confirm_delete"),
]
