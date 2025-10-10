
from django.contrib.auth import authenticate, login, logout
import pandas as pd
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CargaMasivaForm
from .models import BienPatrimonial

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

@login_required
def lista_bienes(request):
    bienes = BienPatrimonial.objects.all().order_by('-fecha_adquisicion', 'nombre')[:500]
    return render(request, 'bienes/lista_bienes.html', {'bienes': bienes})

@login_required
def carga_masiva_bienes(request):
    """
    Carga masiva desde Excel → TU modelo actual.
    Mapeo:
      - id_patrimonial -> numero_identificacion
      - descripcion -> descripcion
      - marca -> marca
      - modelo -> modelo
      - numero_serie -> numero_serie
      - cantidad -> cantidad (default=1)
      - sector -> servicios
    Completa:
      - nombre: primeros 80 chars de descripcion (o modelo/marca/serie o 'SIN NOMBRE')
      - fecha_adquisicion: hoy
      - origen: 'OMISION'
      - estado: 'ACTIVO'
      - valor_adquisicion: 0
    Update-or-create por numero_identificacion si existe; si no, por (numero_serie + descripcion).
    """
    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                archivo = request.FILES['archivo_excel']
                sector_form = form.cleaned_data.get('sector', '').strip()

                df = pd.read_excel(archivo)
                df.columns = [str(c).strip().lower() for c in df.columns]

                creados = 0
                actualizados = 0
                errores = []

                for idx, row in df.iterrows():
                    try:
                        id_patrimonial = str(row.get('id_patrimonial', '') or '').strip()
                        descripcion = str(row.get('descripcion', '') or '').strip()
                        marca = str(row.get('marca', '') or '').strip()
                        modelo = str(row.get('modelo', '') or '').strip()
                        numero_serie = str(row.get('numero_serie', '') or '').strip()

                        cantidad = row.get('cantidad', 1)
                        # saneo cantidad
                        try:
                            cantidad = int(cantidad) if pd.notna(cantidad) else 1
                            if cantidad < 1:
                                cantidad = 1
                        except Exception:
                            cantidad = 1

                        servicios = (sector_form or str(row.get('sector', '') or '')).strip()
                        nombre = descripcion[:80] if descripcion else (modelo or marca or numero_serie or 'SIN NOMBRE')

                        defaults = {
                            'nombre': nombre,
                            'descripcion': descripcion,
                            'cantidad': cantidad,
                            'servicios': servicios or 'Sin especificar',
                            'marca': marca,
                            'modelo': modelo,
                            'numero_serie': numero_serie,
                            'fecha_adquisicion': date.today(),
                            'origen': 'OMISION',       # cambia a 'COMPRA' si lo prefieren
                            'estado': 'ACTIVO',
                            'valor_adquisicion': 0,
                        }

                        if id_patrimonial:
                            obj, created = BienPatrimonial.objects.update_or_create(
                                numero_identificacion=id_patrimonial,
                                defaults=defaults
                            )
                        else:
                            obj, created = BienPatrimonial.objects.update_or_create(
                                numero_serie=numero_serie,
                                descripcion=descripcion,
                                defaults=defaults
                            )

                        creados += int(created)
                        actualizados += int(not created)

                    except Exception as e:
                        errores.append(f"Fila {idx + 2}: {str(e)}")

                if creados or actualizados:
                    messages.success(
                        request,
                        f'Creados: {creados}, Actualizados: {actualizados}. Errores: {len(errores)}'
                    )
                else:
                    messages.warning(request, 'No se crearon ni actualizaron bienes.')

                if errores:
                    messages.error(request, 'Algunas filas fallaron: ' + ' | '.join(errores[:5]))

                return redirect('lista_bienes')

            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
    else:
        form = CargaMasivaForm()

    return render(request, 'carga_masiva.html', {'form': form})


