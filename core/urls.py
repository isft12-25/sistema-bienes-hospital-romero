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
<<<<<<< HEAD
    path('alta_operador/', views.alta_operador, name='alta_operador'),
    path('operadores.html', views.operadores, name='operadores'),

    # Bienes
=======
    path('alta_operador/', views.alta_operador, name='alta_operador'), 
>>>>>>> f7f1a55d3aad72e49e611876a12111cc64cacbac
    path('bien_confirm_delete/', views.bien_confirm_delete, name='bien_confirm_delete'),
    path('bienes.html', views.bienes, name='bienes'),
<<<<<<< HEAD

    # Base / Reportes (si existen en views.py)
    path('base.html', views.base, name='base'),
    path('reportes/', views.reportes_view, name='reportes'),
]
=======
    path('operadores.html', views.operadores, name='operadores'), 
    path('alta-operadores/', views.alta_operadores, name='alta_operadores'),
    path('reportes/', views.reportes_view, name='reportes')
]
>>>>>>> f7f1a55d3aad72e49e611876a12111cc64cacbac
