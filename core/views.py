from django.contrib.auth import authenticate, login, logout
import pandas as pd
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CargaMasivaForm, BienPatrimonialForm
from core.models import BienPatrimonial
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.messages import get_messages


def _role_route_name(user) -> str:
    """Devuelve el nombre de la ruta según el rol del usuario."""
    # Unificamos para que el home del operador sea siempre 'home_operador'
    if hasattr(user, 'tipo_usuario'):
        return 'home_admin' if user.tipo_usuario == 'admin' else 'home_operador'
    return 'home_admin' if user.is_superuser else 'home_operador'


def _safe_next(request) -> str:
    """Devuelve un 'next' válido (mismo host) y que NO apunte al propio login."""
    nxt = request.GET.get('next') or request.POST.get('next') or ''
    if not nxt:
        return ''
    if url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        login_path = reverse('login')
        if nxt.startswith(login_path):
            return ''
        return nxt
    return ''


# ============= VISTAS =============

# -------------------------
# Helpers de permisos
# -------------------------
def permisos_context(user):
    """
    Devuelve un dict con booleans útiles para templates y lógica:
    - es_admin: True si el user es administrador (tipo_usuario == 'admin' o is_superuser)
    - puede_eliminar: True si puede eliminar bienes (solo admins)
    - puede_gestionar_operadores: True si puede gestionar operadores (solo admins)
    """
    if not getattr(user, "is_authenticated", False):
        return {"es_admin": False, "puede_eliminar": False, "puede_gestionar_operadores": False}

    es_admin = False
    if hasattr(user, "tipo_usuario"):
        es_admin = user.tipo_usuario == "admin" or user.is_superuser
    else:
        es_admin = user.is_superuser

    return {
        "es_admin": es_admin,
        "puede_eliminar": es_admin,
        "puede_gestionar_operadores": es_admin,
    }


# ============================
# AUTENTICACIÓN / INICIO
# ============================


@login_required
def inicio(request):
    """
    Vista de inicio.
    Redirige por rol (admin/operadores). Requiere login.
    """
    return redirect(_role_route_name(request.user))


def login_view(request):
    """
    Vista de login (¡sin @login_required!).
    Evita bucles con 'next' y respeta el destino si es seguro.
    """
    # Si ya está logueado, mandarlo al 'next' seguro o a su home por rol
    if request.user.is_authenticated:
        nxt = _safe_next(request)
        return redirect(nxt or _role_route_name(request.user))

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        user = authenticate(request, username=usuario, password=contrasena)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            nxt = _safe_next(request)
            return redirect(nxt or _role_route_name(user))
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    # GET: mostrar login con el 'next' saneado (si vino)
    return render(request, 'login.html', {'next': _safe_next(request)})


@login_required
def home_operador(request):
    """Dashboard operadores."""
    context = permisos_context(request.user)
    return render(request, 'home_operador.html', context)


def registro(request):
    """Vista de registro (placeholder)."""
    return render(request, 'registro.html')


def bien_confirm_delete(request):
    """Plantilla de confirmación de borrado (placeholder)."""
    return render(request, 'bien_confirm_delete.html')


def base(request):
    """Layout base."""
    return render(request, 'base.html')


@login_required
def bienes(request):
    """
    Vista para crear bienes (si el template lo permite).
    Pasamos permisos al template para controlar la UI.
    """
    if request.method == "POST":
        form = BienPatrimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bien creado correctamente.")
            return redirect("lista_bienes")
        messages.error(request, "Revisá los datos del formulario.")
    else:
        form = BienPatrimonialForm()

    context = permisos_context(request.user)
    context.update({"form": form})
    return render(request, "bienes.html", context)


def logout_view(request):
    """Cerrar sesión."""
    logout(request)
    # consumir/limpiar mensajes previos para que no se acumulen
    list(get_messages(request))
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('inicio')


# ============================
# ÁREA PRIVADA (requiere login)
# ============================

@login_required
def home_admin(request):
    """Dashboard administradores."""
    perms = permisos_context(request.user)
    if not perms["es_admin"]:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('home_operador')
    context = perms
    # Puedes añadir métricas al context (total bienes, etc)
    return render(request, 'home_admin.html', context)


@login_required
def operadores(request):
    """Dashboard operadores / gestión de operadores (solo admin puede gestionar)."""
    perms = permisos_context(request.user)
    if not perms["puede_gestionar_operadores"]:
        # Si no es admin, mostrar el dashboard de operador o propio perfil
        messages.warning(request, 'No tienes permisos para gestionar operadores')
        return redirect('home_operador')
    context = perms
    return render(request, 'operadores.html', context)


def recuperar_password(request):
    """Recuperar contraseña (placeholder)."""
    return render(request, 'recuperar_password.html')


@login_required
def alta_operadores(request):
    """Alta/gestión operadores. Solo admin puede crear (backend protegido)."""
    perms = permisos_context(request.user)
    if not perms["puede_gestionar_operadores"]:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('home_operador')

    if request.method == "POST":
        # Lógica mínima de creación (puedes reemplazar con un Form)
        nombre = (request.POST.get('nombre') or "").strip()
        apellido = (request.POST.get('apellido') or "").strip()
        email = (request.POST.get('email') or "").strip()
        password = (request.POST.get('password') or "").strip()
        if not (nombre and apellido and email and password):
            messages.error(request, "Faltan datos obligatorios.")
            return redirect('alta_operadores')

        # Evitar duplicados por email/username
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Ya existe un usuario con ese email/username.")
            return redirect('alta_operadores')

        # Crear usuario (si el modelo User no acepta tipo_usuario, se ignorará ese kw en create_user)
        try:
            user = User.objects.create_user(username=email, email=email, password=password, tipo_usuario='operador', is_active=True)
        except TypeError:
            # modelo auth.User clásico no acepta tipo_usuario
            user = User.objects.create_user(username=email, email=email, password=password, is_active=True)

        # Crear instancia Operador si el modelo existe
        try:
            from core.models.operador import Operador as OperadorModel
            OperadorModel.objects.create(usuario=user, nombre_completo=f"{nombre} {apellido}")
        except (ImportError, AttributeError):
            # Si no existe modelo Operador, continuar sin fallo
            pass

        messages.success(request, "Operador creado correctamente.")
        return redirect('operadores')

    context = perms
    return render(request, 'alta_operadores.html', context)


@login_required
def reportes_view(request):
    """Reportes (placeholder)."""
    context = permisos_context(request.user)
    # modelar reportes y añadirlos al context si hace falta
    context.update({"reportes": []})
    return render(request, 'reportes.html', context)


# ============================
# BIENES - LISTA GENERAL
# ============================

@login_required
def lista_bienes(request):
    q        = (request.GET.get("q") or "").strip()
    f_origen = request.GET.get("f_origen") or ""
    f_estado = request.GET.get("f_estado") or ""
    f_desde  = request.GET.get("f_desde") or ""
    f_hasta  = request.GET.get("f_hasta") or ""
    orden    = request.GET.get("orden") or "-fecha"

    bienes_queryset = (
        BienPatrimonial.objects
        .select_related("expediente")
        .order_by("clave_unica")
    )

    if q:
        bienes_queryset = bienes_queryset.filter(
            Q(clave_unica__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(observaciones__icontains=q) |
            Q(numero_identificacion__icontains=q) |
            Q(servicios__icontains=q) |
            Q(cuenta_codigo__icontains=q) |
            Q(nomenclatura_bienes__icontains=q) |
            Q(numero_serie__icontains=q) |
            Q(origen__icontains=q) |
            Q(estado__icontains=q) |
            Q(expediente__numero_expediente__icontains=q) |
            Q(expediente__numero_compra__icontains=q)
        )

    # Filtro origen
    if f_origen == "__NULL__":
        bienes_queryset = bienes_queryset.filter(origen__isnull=True)
    elif f_origen:
        bienes_queryset = bienes_queryset.filter(origen=f_origen)

    # Filtro estado
    if f_estado == "__NULL__":
        bienes_queryset = bienes_queryset.filter(estado__isnull=True)
    elif f_estado:
        bienes_queryset = bienes_queryset.filter(estado=f_estado)

    # Rango fechas (alta)
    if f_desde:
        d = parse_date(f_desde)
        if d:
            bienes_queryset = bienes_queryset.filter(fecha_adquisicion__gte=d)
    if f_hasta:
        h = parse_date(f_hasta)
        if h:
            bienes_queryset = bienes_queryset.filter(fecha_adquisicion__lte=h)

    # Orden
    if orden == "fecha":
        bienes_queryset = bienes_queryset.order_by("fecha_adquisicion", "clave_unica")
    elif orden == "-fecha":
        bienes_queryset = bienes_queryset.order_by("-fecha_adquisicion", "clave_unica")
    elif orden == "precio":
        bienes_queryset = bienes_queryset.order_by("valor_adquisicion", "clave_unica")
    elif orden == "-precio":
        bienes_queryset = bienes_queryset.order_by("-valor_adquisicion", "clave_unica")
    else:
        bienes_queryset = bienes_queryset.order_by("clave_unica")

    context = permisos_context(request.user)
    context.update({"bienes": bienes_queryset, "q": q})
    return render(request, "bienes/lista_bienes.html", context)


# ============================
# CRUD SIMPLE
# ============================

@login_required
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
    context = permisos_context(request.user)
    context.update({'form': form, 'bien': bien})
    return render(request, 'bienes/editar_bien.html', context)


@login_required
def eliminar_bien(request, pk):
    """Eliminación física directa (no baja). Solo administradores pueden eliminar."""
    perms = permisos_context(request.user)
    if not perms["puede_eliminar"]:
        messages.error(request, "No tienes permisos para eliminar bienes.")
        return redirect('lista_bienes')

    bien = get_object_or_404(BienPatrimonial, pk=pk)
    bien.delete()
    messages.success(request, "Bien eliminado correctamente.")
    return redirect('lista_bienes')


# ============================
# CARGA MASIVA
# ============================

@login_required
def carga_masiva_bienes(request):
    if request.method != 'POST':
        context = permisos_context(request.user)
        context.update({'form': CargaMasivaForm()})
        return render(request, 'carga_masiva.html', context)

    form = CargaMasivaForm(request.POST, request.FILES)
    if not form.is_valid():
        context = permisos_context(request.user)
        context.update({'form': form})
        return render(request, 'carga_masiva.html', {'form': form})

    try:
        archivo = request.FILES['archivo_excel']
        sector_form = (form.cleaned_data.get('sector') or '').strip()

        # 1) Leer Excel preservando texto tal cual
        df = pd.read_excel(archivo, dtype=str)
        df.columns = [str(c).strip().lower() for c in df.columns]

        # Helpers
        def s(v: object) -> str:
            if v is None:
                return ''
            txt = str(v).strip()
            return '' if txt.lower() == 'nan' else txt

        def get_first(row, names) -> str:
            for n in names:
                if n in df.columns:
                    return s(row.get(n))
            return ''

        def to_int1(v) -> int:
            txt = s(v)
            if not txt:
                return 1
            try:
                val = int(float(txt))
                return max(val, 1)
            except (ValueError, TypeError):
                return 1

        def parse_money(v):
            txt = s(v)
            if not txt:
                return None
            txt = txt.replace('$', '').replace(' ', '')
            if ',' in txt and txt.rfind(',') > txt.rfind('.'):
                txt = txt.replace('.', '').replace(',', '.')
            else:
                txt = txt.replace(',', '')
            try:
                return Decimal(txt)
            except InvalidOperation:
                return None

        def parse_date_any(v):
            txt = s(v)
            if not txt:
                return None
            try:
                dt = pd.to_datetime(txt, errors='coerce', dayfirst=True)
                if pd.isna(dt):
                    return None
                return dt.date()
            except (ValueError, TypeError):
                return None

        def map_origen(v):
            t = s(v).lower()
            if not t:
                return None
            if 'compra' in t or 'minister' in t:
                return 'COMPRA'
            if 'donac' in t:
                return 'DONACION'
            if 'omisi' in t:
                return 'OMISION'
            if 'transfer' in t or 'traslad' in t:
                return 'TRANSFERENCIA'
            return None

        def map_estado(v):
            t = s(v).lower()
            if not t:
                return None
            if 'manten' in t:
                return 'MANTENIMIENTO'
            if 'baja' in t:
                return 'BAJA'
            if 'inac' in t:
                return 'INACTIVO'
            if 'activ' in t:
                return 'ACTIVO'
            return None

        creados, actualizados, errores = 0, 0, []

        from core.models import Expediente  # import local

        with transaction.atomic():
            for i, row in df.iterrows():
                try:
                    numero_id   = get_first(row, ['n de id','n_de_id','numero_identificacion','id_patrimonial','nº de id','no de id'])
                    nro_exp     = get_first(row, ['n de expediente','n_de_expediente','numero_expediente','nº de expediente','no de expediente','expediente'])
                    nro_compra  = get_first(row, ['n de compra','n_de_compra','numero_compra','nº de compra','no de compra'])
                    nro_serie   = get_first(row, ['n de serie','n_de_serie','numero_serie','nº de serie','no de serie'])
                    descripcion = get_first(row, ['descripcion','descripción','descripcion_del_bien'])

                    cantidad    = to_int1(get_first(row, ['cantidad']))
                    servicios   = s(get_first(row, ['servicios','sector']) or sector_form) or 'Sin especificar'
                    cuenta_cod  = get_first(row, ['cuenta codigo','cuenta_código','cuenta_codigo'])
                    nomencl     = get_first(row, ['nomenclatura de bienes','nomenclatura_de_bienes','nomenclatura_bienes'])
                    observ      = get_first(row, ['observaciones','obs'])

                    origen_txt  = get_first(row, ['origen'])
                    estado_txt  = get_first(row, ['estado'])
                    precio_raw  = get_first(row, ['precio','valor','importe'])

                    fecha_alta  = parse_date_any(get_first(row, ['fecha de alta','fecha_de_alta','fecha_alta']))
                    fecha_baja  = parse_date_any(get_first(row, ['fecha de baja','fecha_de_baja','fecha_baja']))

                    origen = map_origen(origen_txt)
                    estado = map_estado(estado_txt)

                    precio = parse_money(precio_raw)
                    if origen != 'COMPRA':
                        precio = None

                    if not fecha_alta:
                        fecha_alta = date.today()

                    expediente_obj = None
                    if nro_exp:
                        expediente_obj, _ = Expediente.objects.get_or_create(
                            numero_expediente=nro_exp
                        )
                        if nro_compra:
                            expediente_obj.numero_compra = nro_compra
                            expediente_obj.save(update_fields=['numero_compra'])

                    nombre = (descripcion[:200] if descripcion else (nro_serie or 'SIN NOMBRE'))

                    defaults = {
                        'nombre': nombre,
                        'descripcion': descripcion,
                        'cantidad': cantidad,
                        'servicios': servicios,
                        'numero_serie': nro_serie,
                        'cuenta_codigo': cuenta_cod,
                        'nomenclatura_bienes': nomencl,
                        'observaciones': observ,
                        'origen': origen,
                        'estado': estado,
                        'valor_adquisicion': precio,
                        'fecha_adquisicion': fecha_alta,
                        'fecha_baja': fecha_baja,
                        'expediente': expediente_obj,
                    }

                    if numero_id:
                        _, created = BienPatrimonial.objects.update_or_create(
                            numero_identificacion=numero_id,
                            defaults=defaults
                        )
                    elif nro_serie and descripcion:
                        _, created = BienPatrimonial.objects.update_or_create(
                            numero_serie=nro_serie,
                            descripcion=descripcion,
                            defaults=defaults
                        )
                    else:
                        BienPatrimonial.objects.create(**defaults)
                        created = True

                    creados += int(created)
                    actualizados += int(not created)

                except (ValueError, ValidationError, IntegrityError) as e:
                    errores.append(f"Fila {i + 2}: {e}")

        if creados or actualizados:
            messages.success(
                request,
                f'Creados: {creados}, Actualizados: {actualizados}. Errores: {len(errores)}'
            )
        else:
            messages.warning(request, 'No se crearon ni actualizaron bienes.')

        if errores:
            messages.error(request, 'Algunas filas fallaron: ' + ' | '.join(errores[:8]))

        return redirect('lista_bienes')

    except (FileNotFoundError, pd.errors.EmptyDataError, KeyError) as e:
        messages.error(request, f'Error al procesar el archivo: {e}')
        return redirect('lista_bienes')


@login_required
@require_POST
def eliminar_bienes_seleccionados(request):
    perms = permisos_context(request.user)
    if not perms["puede_eliminar"]:
        messages.error(request, "No tienes permisos para eliminar bienes.")
        return redirect('lista_bienes')

    ids = request.POST.getlist('seleccionados')
    if not ids:
        messages.warning(request, "No seleccionaste bienes para eliminar.")
        return redirect('lista_bienes')

    eliminados = BienPatrimonial.objects.filter(pk__in=ids).delete()[0]
    messages.success(request, f"Eliminados: {eliminados}")
    return redirect('lista_bienes')


# ============================
# BAJAS
# ============================

@login_required
def lista_baja_bienes(request):
    """Lista de bienes con estado BAJA."""
    q = (request.GET.get("q") or "").strip()
    orden = request.GET.get("orden") or "-fecha_baja"

    bienes_baja = (
        BienPatrimonial.objects
        .select_related("expediente")
        .filter(estado="BAJA")
    )

    if q:
        bienes_baja = bienes_baja.filter(
            Q(clave_unica__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(observaciones__icontains=q) |
            Q(descripcion_baja__icontains=q) |
            Q(numero_identificacion__icontains=q) |
            Q(servicios__icontains=q) |
            Q(cuenta_codigo__icontains=q) |
            Q(nomenclatura_bienes__icontains=q) |
            Q(numero_serie__icontains=q) |
            Q(expediente__numero_expediente__icontains=q) |
            Q(expediente_baja__icontains=q)
        )

    if orden == "fecha_baja":
        bienes_baja = bienes_baja.order_by("fecha_baja", "clave_unica")
    elif orden == "-fecha_baja":
        bienes_baja = bienes_baja.order_by("-fecha_baja", "clave_unica")
    elif orden == "precio":
        bienes_baja = bienes_baja.order_by("valor_adquisicion", "clave_unica")
    elif orden == "-precio":
        bienes_baja = bienes_baja.order_by("-valor_adquisicion", "clave_unica")
    else:
        bienes_baja = bienes_baja.order_by("-fecha_baja", "clave_unica")

    context = permisos_context(request.user)
    context.update({"bienes": bienes_baja})
    return render(request, "bienes/lista_baja_bienes.html", context)


@login_required
@require_POST
def dar_baja_bien(request, pk):
    """
    Marca un bien como BAJA y guarda datos de baja.
    Espera POST con: fecha_baja, expediente_baja, descripcion_baja.
    """
    bien = get_object_or_404(BienPatrimonial, pk=pk)

    fecha_baja = parse_date(request.POST.get("fecha_baja") or "") or date.today()
    expediente_baja = (request.POST.get("expediente_baja") or "").strip()
    descripcion_baja = (request.POST.get("descripcion_baja") or "").strip()

    bien.estado = "BAJA"
    bien.fecha_baja = fecha_baja

    if hasattr(bien, "expediente_baja"):
        bien.expediente_baja = expediente_baja
    if hasattr(bien, "descripcion_baja"):
        bien.descripcion_baja = descripcion_baja
    elif descripcion_baja:
        bien.observaciones = (bien.observaciones or "")
        if bien.observaciones:
            bien.observaciones += " | "
        bien.observaciones += f"BAJA: {descripcion_baja}"

    bien.save()
    messages.success(request, f"Bien {bien.clave_unica or bien.pk} dado de baja correctamente.")
    return redirect("lista_baja_bienes")


@login_required
@require_POST
@transaction.atomic
def restablecer_bien(request, pk):
    """
    Restablece un bien dado de baja:
    - estado = 'ACTIVO'
    - limpia fecha_baja / expediente_baja / descripcion_baja si existen
    Solo administradores pueden restablecer.
    """
    perms = permisos_context(request.user)
    if not perms["es_admin"]:
        messages.error(request, "No tienes permisos para restablecer bienes.")
        return redirect("lista_baja_bienes")

    bien = get_object_or_404(BienPatrimonial, pk=pk)

    bien.estado = "ACTIVO"
    if hasattr(bien, "fecha_baja"):
        bien.fecha_baja = None
    if hasattr(bien, "expediente_baja"):
        bien.expediente_baja = None
    if hasattr(bien, "descripcion_baja"):
        bien.descripcion_baja = ""

    update_fields = ["estado"]
    if hasattr(bien, "fecha_baja"):
        update_fields.append("fecha_baja")
    if hasattr(bien, "expediente_baja"):
        update_fields.append("expediente_baja")
    if hasattr(bien, "descripcion_baja"):
        update_fields.append("descripcion_baja")

    bien.save(update_fields=update_fields)
    messages.success(request, f"Bien {bien.clave_unica or bien.pk} restablecido a ACTIVO.")
    return redirect("lista_bienes")


@login_required
@require_POST
@transaction.atomic
def eliminar_bien_definitivo(request, pk):
    """
    Elimina físicamente un bien (no reversible). Se usa desde lista de bajas.
    Solo administradores pueden eliminar definitivamente.
    """
    perms = permisos_context(request.user)
    if not perms["es_admin"]:
        messages.error(request, "No tienes permisos para eliminar bienes definitivamente.")
        return redirect("lista_baja_bienes")

    bien = get_object_or_404(BienPatrimonial, pk=pk)
    identificador = bien.clave_unica or bien.pk
    bien.delete()
    messages.success(request, f"Bien {identificador} eliminado definitivamente.")
    return redirect("lista_baja_bienes")