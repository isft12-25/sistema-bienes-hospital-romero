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
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('home_admin/', views.home_admin, name='home_admin'),  # 👈 Ruta para el dashboard
>>>>>>> d3a3fd8fbbadc8fa7b9dc0494193b2dbe96a2e20
]
