from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('home_admin/', views.home_admin, name='home_admin'),
    path('alta_operador/', views.alta_operador, name='alta_operador'), #Reemplazo de home_empleado
    path('bien_confirm_delete/', views.bien_confirm_delete, name='bien_confirm_delete'),
    path('base.html', views.base, name='base'),
    path('bienes.html', views.bienes_patrimoniales, name='bienes'),
    path('operadores.html', views.operadores, name='operadores'),  # 👈 Ruta para el dashboard
    path('alta-operadores/', views.alta_operadores, name='alta_operadores'),
    path('reportes/', views.reportes_view, name='reportes')
]