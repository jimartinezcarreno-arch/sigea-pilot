from django.conf import settings
from django.http import HttpResponseForbidden

from .permissions import tiene_rol


class RoleAccessMiddleware:
    """Aplica permisos de escritura a los puntos sensibles del piloto."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.REQUIRE_LOGIN or not request.user.is_authenticated:
            return self.get_response(request)

        ruta = request.path_info
        puede_programar = tiene_rol(request.user, 'ADMIN', 'PROGRAMADOR')
        puede_administrar = tiene_rol(request.user, 'ADMIN')

        if ruta == '/usuarios/' and not puede_administrar:
            return HttpResponseForbidden('Solo el administrador institucional puede gestionar usuarios.')

        if request.method == 'POST' and (
            ruta == '/subir-excel/' or ruta.startswith('/conflictos/reasignar/')
        ) and not puede_programar:
            return HttpResponseForbidden('Tu rol no puede modificar la programaci\u00f3n.')

        return self.get_response(request)
