from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('home_admin/', views.home_admin, name='home_admin'),  # 👈 Ruta para el dashboard
]
