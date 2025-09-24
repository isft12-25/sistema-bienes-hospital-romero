from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='inicio.html'), name='inicio'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('recuperar-password/', TemplateView.as_view(template_name='recuperar_password.html'), name='recuperar_password'),
    path('dashboard/', TemplateView.as_view(template_name='home_admin.html'), name='dashboard'),
]
