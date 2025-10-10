
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def inicio(request):
    """
    Vista de inicio.
    - Si el usuario YA está autenticado, redirige según su tipo de usuario.
    - Admin -> 'home_admin'
    - Resto -> 'operadores'
    - Si no está autenticado, renderiza 'inicio.html'
    """
    if request.user.is_authenticated:
        # Si el modelo de usuario tiene el atributo 'tipo_usuario' (custom)
        if hasattr(request.user, 'tipo_usuario'):
            if request.user.tipo_usuario == 'admin':
                return redirect('home_admin')
            else:
                return redirect('operadores')
        else:
            # Compatibilidad: superusuario sin tipo_usuario → admin
            if request.user.is_superuser:
                return redirect('home_admin')
            else:
                return redirect('operadores')

    return render(request, 'inicio.html')


def login_view(request):
    """
    Vista de login.
    - Si ya está logueado, redirige según el tipo de usuario (igual que en 'inicio').
    - Si viene por POST, intenta autenticar con 'usuario' y 'contrasena'.
    - Al autenticar, redirige según el tipo de usuario.
    - Si falla, muestra mensaje de error y vuelve al form.
    """
    # Usuario ya autenticado → redirigir (evita re-logins innecesarios)
    if request.user.is_authenticated:
        if hasattr(request.user, 'tipo_usuario'):
            if request.user.tipo_usuario == 'admin':
                return redirect('home_admin')
            else:
                return redirect('operadores')
        else:
            if request.user.is_superuser:
                return redirect('home_admin')
            else:
                return redirect('operadores')

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        # Autenticar usuario (por username y password)
        user = authenticate(request, username=usuario, password=contrasena)

        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')

            # Redirección por rol/tipo
            if hasattr(user, 'tipo_usuario'):
                if user.tipo_usuario == 'admin':
                    return redirect('home_admin')
                else:
                    return redirect('operadores')
            else:
                if user.is_superuser:
                    return redirect('home_admin')
                else:
                    return redirect('operadores')
        else:
            # Credenciales inválidas
            messages.error(request, 'Usuario o contraseña incorrectos')

    # GET o POST inválido → mostrar formulario
    return render(request, 'login.html')

def registro(request):
    """
    Vista de registro de usuario (formulario estático/placeholder).
    """
    return render(request, 'registro.html')


def alta_operador(request):
    """
    Vista para dar de alta un operador (formulario estático/placeholder).
    """
    return render(request, 'alta_operador.html')


def bien_confirm_delete(request):
    """
    Vista para confirmar el borrado de un bien patrimonial (plantilla estática).
    """
    return render(request, 'bien_confirm_delete.html')


def base(request):
    """
    Render de la plantilla base (layout).
    """
    return render(request, 'base.html')


def bienes(request):
    """
    Vista para listar/visualizar bienes (plantilla estática/placeholder).
    """
    return render(request, 'bienes.html')

def logout_view(request):
    """
    Cerrar sesión:
    - Cierra la sesión actual.
    - Muestra un mensaje de éxito.
    - Redirige a 'inicio'.
    """
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('inicio')


# ============================
# ÁREA PRIVADA (requiere login)
# ============================

@login_required
def home_admin(request):
    """
    Dashboard para administradores (requiere autenticación).
    - Valida que el usuario tenga permisos de admin:
      * tipo_usuario == 'admin'  ó
      * sea superusuario
    - Si no, redirige a 'operadores' con mensaje de error.
    """
    # Validación de permisos por atributo custom
    if hasattr(request.user, 'tipo_usuario'):
        if request.user.tipo_usuario != 'admin':
            messages.error(request, 'No tienes permisos para acceder a esta página')
            return redirect('operadores')
    # Compatibilidad: usuario sin 'tipo_usuario', verificar superusuario
    elif not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('operadores')

    return render(request, 'home_admin.html')


@login_required
def operadores(request):
    """
    Dashboard para empleados del hospital (2ª definición).
    NOTA IMPORTANTE:
      - Esta definición *sustituye* a la anterior con el mismo nombre.
      - Tiene @login_required → exige autenticación para acceder.
    """
    return render(request, 'operadores.html')


def recuperar_password(request):
    """
    Vista de recuperación de contraseña (2ª definición).
    NOTA IMPORTANTE:
      - Esta definición *sustituye* a la primera que aparece arriba.
      - Efecto final: esta es la función activa que Django usará.
    """
    return render(request, 'recuperar_password.html')


def alta_operadores(request):
    """
    Vista para alta masiva o gestión de operadores (plantilla estática/placeholder).
    """
    return render(request, 'alta_operadores.html')


def reportes_view(request):
    """
    Vista de reportes (plantilla estática/placeholder).
    """
    return render(request, 'reportes.html')
