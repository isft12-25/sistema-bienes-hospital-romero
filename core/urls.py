from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('bienes/', views.lista_bienes, name='lista_bienes'),
]