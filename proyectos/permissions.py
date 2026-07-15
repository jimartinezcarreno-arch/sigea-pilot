from functools import wraps

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden


def _perfil_activo(usuario):
    try:
        return usuario.perfil_sigea if usuario.perfil_sigea.activo else None
    except AttributeError:
        return None


def tiene_rol(usuario, *roles):
    """Indica si una cuenta puede realizar una acci\u00f3n dentro de su instituci\u00f3n."""
    if not usuario.is_authenticated:
        return False
    if usuario.is_superuser:
        return True
    perfil = _perfil_activo(usuario)
    return bool(perfil and perfil.rol in roles)


def es_administrador_institucional(usuario):
    return tiene_rol(usuario, 'ADMIN')


def roles_requeridos(*roles):
    """Protege vistas de escritura sin alterar la experiencia local sin login."""
    def decorador(vista):
        @wraps(vista)
        def envuelta(request, *args, **kwargs):
            if not settings.REQUIRE_LOGIN:
                return vista(request, *args, **kwargs)
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
            if not tiene_rol(request.user, *roles):
                return HttpResponseForbidden('No tienes permisos para realizar esta acci\u00f3n.')
            return vista(request, *args, **kwargs)
        return envuelta
    return decorador
