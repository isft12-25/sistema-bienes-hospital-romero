from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def inicio(request):
    """Vista de inicio - muestra opciones de login"""
    # Si ya está logueado, redirigir según tipo de usuario
    if request.user.is_authenticated:
        # Verificar si el usuario tiene el atributo tipo_usuario
        if hasattr(request.user, 'tipo_usuario'):
            if request.user.tipo_usuario == 'admin':
                return redirect('home_admin')
            else:
                return redirect('home_empleado')
        else:
            # Si es un superusuario sin tipo_usuario (usuario antiguo)
            if request.user.is_superuser:
                return redirect('home_admin')
            else:
                return redirect('home_empleado')
    
    return render(request, 'inicio.html')


def login_view(request):
    """Vista de login - procesa el inicio de sesión"""
    # Si ya está logueado, redirigir
    if request.user.is_authenticated:
        if hasattr(request.user, 'tipo_usuario'):
            if request.user.tipo_usuario == 'admin':
                return redirect('home_admin')
            else:
                return redirect('home_empleado')
        else:
            if request.user.is_superuser:
                return redirect('home_admin')
            else:
                return redirect('home_empleado')
    
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        
        # Autenticar usuario
        user = authenticate(request, username=usuario, password=contrasena)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            
            # Redirigir según tipo de usuario
            if hasattr(user, 'tipo_usuario'):
                if user.tipo_usuario == 'admin':
                    return redirect('home_admin')
                else:
                    return redirect('home_empleado')
            else:
                # Usuario sin tipo_usuario
                if user.is_superuser:
                    return redirect('home_admin')
                else:
                    return redirect('home_empleado')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')


def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('inicio')


@login_required
def home_admin(request):
    """Dashboard para administradores"""
    # Verificar permisos
    if hasattr(request.user, 'tipo_usuario'):
        if request.user.tipo_usuario != 'admin':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('home_empleado')
    elif not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('home_empleado')
    
    return render(request, 'home_admin.html')


@login_required
def home_empleado(request):
    """Dashboard para empleados del hospital"""
    return render(request, 'home_empleado.html')


def recuperar_password(request):
    """Vista de recuperación de contraseña"""
    return render(request, 'recuperar_password.html')