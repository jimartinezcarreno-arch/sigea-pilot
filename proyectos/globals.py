import threading

# Almacenar la request actual en un hilo local para que TenantManager pueda acceder
_thread_local = threading.local()

def get_current_request():
    """Retorna la request almacenada en el thread local."""
    return getattr(_thread_local, 'request', None)

def set_current_request(request):
    """Almacena la request en el thread local."""
    _thread_local.request = request

def clear_current_request():
    """Limpia la request del thread local."""
    if hasattr(_thread_local, 'request'):
        del _thread_local.request