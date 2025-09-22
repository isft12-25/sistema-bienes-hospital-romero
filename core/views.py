from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Vista para la página de inicio"""
    return render(request, 'core/inicio/home.html')

def login_view(request):
    """Vista para la página de login"""
    return render(request, 'login.html')
	
def lista_bienes(request):
    return HttpResponse("Lista de bienes patrimoniales")

def Expediente_list(request):
    return HttpResponse("Lista de expedientes")