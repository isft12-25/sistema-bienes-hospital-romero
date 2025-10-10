from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('home_admin/', views.home_admin, name='home_admin'),
    path('bien_confirm_delete/', views.bien_confirm_delete, name='bien_confirm_delete'),
    path('base/', views.base, name='base'),
    path('bienes/', views.bienes, name='bienes'),
    path('operadores/', views.operadores, name='operadores'), 
    path('alta-operadores/', views.alta_operadores, name='alta_operadores'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('lista-bienes/', views.lista_bienes, name='lista_bienes'),
    path('carga-masiva/', views.carga_masiva_bienes, name='carga_masiva'),
]