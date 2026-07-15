from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .models import PerfilUsuario
from .permissions import roles_requeridos
from .tenant_utils import get_current_institucion


@roles_requeridos('ADMIN')
@require_http_methods(['GET', 'POST'])
def gestionar_usuarios(request):
    institucion = get_current_institucion()
    if institucion is None:
        messages.error(request, 'No se encontr\u00f3 una instituci\u00f3n activa para administrar usuarios.')
        return redirect('consulta_aulas')

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'crear':
            _crear_usuario(request, institucion)
        elif accion == 'cambiar_estado':
            _cambiar_estado(request, institucion)
        else:
            messages.error(request, 'La acci\u00f3n solicitada no es v\u00e1lida.')
        return redirect('gestionar_usuarios')

    perfiles = PerfilUsuario.objects.filter(institucion=institucion).select_related('user').order_by(
        'rol', 'user__username'
    )
    return render(request, 'gestion_usuarios.html', {
        'institucion_activa': institucion,
        'perfiles': perfiles,
        'roles': PerfilUsuario.ROL_CHOICES,
    })


def _crear_usuario(request, institucion):
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    rol = request.POST.get('rol', 'CONSULTA')
    roles_validos = {valor for valor, _ in PerfilUsuario.ROL_CHOICES}

    if not username or not password:
        messages.error(request, 'El usuario y la contrase\u00f1a temporal son obligatorios.')
        return
    if rol not in roles_validos:
        messages.error(request, 'Selecciona un rol v\u00e1lido.')
        return

    User = get_user_model()
    if User.objects.filter(username__iexact=username).exists():
        messages.error(request, 'Ya existe una cuenta con ese usuario.')
        return

    try:
        validate_password(password)
    except ValidationError as error:
        messages.error(request, ' '.join(error.messages))
        return

    with transaction.atomic():
        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True,
        )
        PerfilUsuario.objects.create(
            user=usuario,
            institucion=institucion,
            rol=rol,
            activo=True,
        )

    messages.success(request, f"Cuenta creada para {username}. Comparte la contrase\u00f1a por un canal seguro.")


def _cambiar_estado(request, institucion):
    perfil_id = request.POST.get('perfil_id')
    perfil = PerfilUsuario.objects.filter(id=perfil_id, institucion=institucion).select_related('user').first()
    if perfil is None:
        messages.error(request, 'No se encontr\u00f3 la cuenta solicitada.')
        return
    if perfil.user_id == request.user.id:
        messages.error(request, 'No puedes desactivar tu propia cuenta desde esta pantalla.')
        return

    perfil.activo = not perfil.activo
    perfil.user.is_active = perfil.activo
    perfil.user.save(update_fields=['is_active'])
    perfil.save(update_fields=['activo'])
    estado = 'activada' if perfil.activo else 'desactivada'
    messages.success(request, f"La cuenta de {perfil.user.username} fue {estado}.")
