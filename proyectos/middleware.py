import os

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden

from .tenant_utils import get_current_institucion, set_current_institucion
from .models import Institucion

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Obtener el host (ej: uniminuto.sigea.com o localhost:8000)
        host = request.get_host().split(':')[0]
        
        # 2. Extraer el subdominio (ej: 'uniminuto')
        host_parts = host.split('.')
        
        # Si estás en localhost o tienes un dominio completo:
        primary_tenant_host = os.environ.get('PRIMARY_TENANT_HOST')
        if host in {'localhost', '127.0.0.1', '0.0.0.0', 'testserver'} or host == primary_tenant_host:
            # Mantiene una instituciÃ³n de desarrollo/piloto explÃ­cita sin abrir datos en hosts desconocidos.
            subdominio_actual = os.environ.get('DEFAULT_TENANT_SUBDOMAIN', 'sigea')
        elif len(host_parts) > 1 and host_parts[0] != 'www':
            subdominio_actual = host_parts[0]
        else:
            subdominio_actual = None

        try:
            # 3. Buscar la institución en la base de datos
            institucion = Institucion.objects.get(subdominio=subdominio_actual, activo=True)
            # 4. Registrarla en el hilo seguro para que models.py la use de forma invisible
            set_current_institucion(institucion)
        except (Institucion.DoesNotExist, TypeError):
            set_current_institucion(None)

        response = self.get_response(request)
        
        # 5. Limpiar al terminar la petición HTTP
        set_current_institucion(None)
        return response


class TenantAccessMiddleware:
    """Exige autenticaciÃ³n y valida la pertenencia al tenant cuando se activa el piloto."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.REQUIRE_LOGIN:
            return self.get_response(request)

        ruta_publica = request.path_info in {settings.LOGIN_URL, '/salir/'}
        if ruta_publica:
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)

        if request.user.is_superuser:
            return self.get_response(request)

        institucion = get_current_institucion()
        perfil = getattr(request.user, 'perfil_sigea', None)
        if not institucion or not perfil or not perfil.activo or perfil.institucion_id != institucion.id:
            return HttpResponseForbidden('No tienes acceso a esta instituciÃ³n.')

        return self.get_response(request)
