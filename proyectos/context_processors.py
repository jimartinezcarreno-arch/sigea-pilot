from django.conf import settings

from .permissions import tiene_rol


def contexto_acceso_sigea(request):
    """Expone el nivel de acceso actual a las plantillas sin duplicar lógica."""
    usuario = request.user
    autenticado = usuario.is_authenticated
    perfil = None
    if autenticado and not usuario.is_superuser:
        try:
            perfil = usuario.perfil_sigea
        except AttributeError:
            perfil = None

    if usuario.is_superuser:
        etiqueta_rol = 'Administrador global'
    elif perfil:
        etiqueta_rol = perfil.get_rol_display()
    elif autenticado:
        etiqueta_rol = 'Cuenta sin perfil'
    else:
        etiqueta_rol = 'Acceso local'

    return {
        'sigea_access': {
            'is_authenticated': autenticado,
            'role_label': etiqueta_rol,
            'can_programar': not settings.REQUIRE_LOGIN or tiene_rol(usuario, 'ADMIN', 'PROGRAMADOR'),
            'can_administrar': tiene_rol(usuario, 'ADMIN'),
        },
    }
