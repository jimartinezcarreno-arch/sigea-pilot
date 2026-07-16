from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from proyectos.access_views import gestionar_usuarios
from proyectos.import_views import historial_importaciones, restaurar_importacion, subir_programacion_segura

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('subir-excel/', subir_programacion_segura, name='subir_programacion_segura'),
    path('importaciones/', historial_importaciones, name='historial_importaciones'),
    path('importaciones/<int:importacion_id>/restaurar/', restaurar_importacion, name='restaurar_importacion'),
    path('', include('proyectos.urls')),  # Incluye todas las rutas de la app 'proyectos'
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
