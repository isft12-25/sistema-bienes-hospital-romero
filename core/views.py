from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Sistema de Gestión de Bienes Patrimoniales - Hospital Melchor Romero!")

def lista_bienes(request):
    return HttpResponse("Lista de bienes patrimoniales")

def Expediente_list(request):
    return HttpResponse("Lista de expedientes")