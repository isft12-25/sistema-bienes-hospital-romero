
from django.contrib.auth import authenticate, login, logout
import pandas as pd
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CargaMasivaForm
from .models import BienPatrimonial
from django.db.models import Q
from .forms import BienPatrimonialForm
from django.views.decorators.http import require_POST


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
    q = (request.GET.get("q") or "").strip()

    bienes = (
        BienPatrimonial.objects
        .select_related("expediente")        # para usar expediente.numero_expediente / numero_compra
        .order_by("clave_unica")
    )

    if q:
        bienes = bienes.filter(
            Q(clave_unica__icontains=q) |
            Q(numero_identificacion__icontains=q) |
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(servicios__icontains=q) |
            Q(cuenta_codigo__icontains=q) |
            Q(nomenclatura_bienes__icontains=q) |
            Q(numero_serie__icontains=q) |
            Q(origen__icontains=q) |
            Q(estado__icontains=q) |
            Q(expediente__numero_expediente__icontains=q) |
            Q(expediente__numero_compra__icontains=q)
        )

    return render(
        request,
        "bienes/lista_bienes.html",
        {"bienes": bienes, "q": q}
    )
def editar_bien(request, pk):
    bien = get_object_or_404(BienPatrimonial, pk=pk)

    if request.method == 'POST':
        form = BienPatrimonialForm(request.POST, instance=bien)
        if form.is_valid():
            form.save()
            messages.success(request, "Bien patrimonial actualizado correctamente.")
            return redirect('lista_bienes')
    else:
        form = BienPatrimonialForm(instance=bien)

    return render(request, 'bienes/editar_bien.html', {'form': form, 'bien': bien})


def eliminar_bien(request, pk): 

    bien = get_object_or_404(BienPatrimonial, pk=pk)
    bien.delete()
    messages.success(request, "Bien eliminado correctamente.")
    return redirect('lista_bienes')




@login_required
def carga_masiva_bienes(request):
    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                archivo = request.FILES['archivo_excel']
                sector_form = form.cleaned_data.get('sector', '').strip()

                # Leer Excel y normalizar encabezados a minúsculas
                df = pd.read_excel(archivo)
                df.columns = [str(c).strip().lower() for c in df.columns]

                creados = 0
                actualizados = 0
                errores = []

                for idx, row in df.iterrows():
                    try:
                        # columnas esperadas en el excel
                        id_patrimonial = str(row.get('id_patrimonial', '') or '').strip()
                        descripcion = str(row.get('descripcion', '') or '').strip()
                        numero_serie = str(row.get('numero_serie', '') or '').strip()

                        # cantidad saneada (>=1)
                        cantidad = row.get('cantidad', 1)
                        try:
                            cantidad = int(cantidad) if pd.notna(cantidad) else 1
                            if cantidad < 1:
                                cantidad = 1
                        except Exception:
                            cantidad = 1

                        # sector/servicio (desde form si no viene en excel)
                        servicios = (sector_form or str(row.get('sector', '') or '')).strip()
                        if not servicios:
                            servicios = 'Sin especificar'

                        # nombre: desde descripción o fallback
                        nombre = descripcion[:200] if descripcion else (numero_serie or 'SIN NOMBRE')

                        # por ahora dejamos origen=OMISION y sin precio
                        defaults = {
                            'numero_identificacion': (str(row.get('numero_identificacion', '') or '').strip()  or None),
                            'nombre': nombre,
                            'descripcion': descripcion,
                            'cantidad': cantidad,
                            'servicios': servicios,
                            'numero_serie': numero_serie,
                            'fecha_adquisicion': date.today(),
                            'origen': 'OMISION',        # si luego querés, cámbialo a 'COMPRA'
                            'estado': 'ACTIVO',
                            'valor_adquisicion': None,  # si no es COMPRA, no hay precio
                            'cuenta_codigo': str(row.get('cuenta_codigo', '') or '').strip(),
                            'nomenclatura_bienes': str(row.get('nomenclatura_bienes', '') or '').strip(),
                           
                        }

                        # clave de actualización:
                        # 1) si viene ID patrimonial (numero_identificacion) => se usa como clave
                        # 2) si no, actualizamos por (numero_serie + descripcion) para evitar duplicados
                        if defaults['numero_identificacion']:
                            obj, created = BienPatrimonial.objects.update_or_create(
                                numero_identificacion=defaults['numero_identificacion'],
                                defaults=defaults
                            )
                        elif numero_serie and descripcion:
                            obj, created = BienPatrimonial.objects.update_or_create(
                                numero_serie=numero_serie,
                                descripcion=descripcion,
                                defaults=defaults
                            )
                        else:
                            # si no hay clave estable, creamos uno nuevo
                            obj = BienPatrimonial.objects.create(**defaults)
                            created = True

                        if created:
                            creados += 1
                        else:
                            actualizados += 1

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

    # RESPETA TU ESTRUCTURA DE TEMPLATES:
    return render(request, 'carga_masiva.html', {'form': form})

@login_required
@require_POST
def eliminar_bienes_seleccionados(request):
    ids = request.POST.getlist('seleccionados')  # viene de los checkboxes
    if not ids:
        messages.warning(request, "No seleccionaste bienes para eliminar.")
        return redirect('lista_bienes')

    eliminados = BienPatrimonial.objects.filter(pk__in=ids).delete()[0]
    messages.success(request, f"Eliminados: {eliminados}")
    return redirect('lista_bienes')