from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')

def login_view(request):
    return render(request, 'login.html')

def recuperar_password(request):
    return render(request, 'recuperar_password.html')

def home_admin(request):
    return render(request, 'home_admin.html')
