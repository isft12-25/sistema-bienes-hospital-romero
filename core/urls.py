from django.urls import path
<<<<<<< HEAD
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='inicio.html'), name='inicio'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('recuperar-password/', TemplateView.as_view(template_name='recuperar_password.html'), name='recuperar_password'),
    path('dashboard/', TemplateView.as_view(template_name='home_admin.html'), name='dashboard'),
=======
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
<<<<<<< HEAD
    path('home_admin/', views.home_admin, name='home_admin'),  # 👈 Ruta para el dashboard
>>>>>>> d3a3fd8fbbadc8fa7b9dc0494193b2dbe96a2e20
]
=======
    path('home_admin/', views.home_admin, name='home_admin'),
    path('alta_operador/', views.alta_operador, name='alta_operador'), #Reemplazo de home_empleado
    path('bien_confirm_delete/', views.bien_confirm_delete, name='bien_confirm_delete'),
    path('base.html', views.base, name='base'),
    path('bienes.html', views.bienes_patrimoniales, name='bienes'),
    path('operadores.html', views.operadores, name='operadores')  # 👈 Ruta para el dashboard
]
>>>>>>> 025d3608897be9129cc58de13b5db1c8dc2d1282
