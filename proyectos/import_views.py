from django.contrib import messages
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Clase, ImportacionProgramacion, Institucion
from .permissions import roles_requeridos
from .services.excel_importer import ExcelImporter
from .services.programacion_backup import capturar_programacion, clases_desde_respaldo
from .tenant_utils import get_current_institucion


def _institucion_activa():
    return get_current_institucion() or Institucion.objects.first()


@roles_requeridos('ADMIN', 'PROGRAMADOR')
@require_POST
def subir_programacion_segura(request):
    archivo = request.FILES.get('archivo_excel')
    if not archivo:
        messages.error(request, 'Selecciona un archivo Excel antes de importar.')
        return redirect('consulta_aulas')

    institucion = _institucion_activa()
    if institucion is None:
        messages.error(request, 'No hay una institución activa para recibir la programación.')
        return redirect('consulta_aulas')

    resultado = ExcelImporter(archivo, institucion, usuario=request.user).importar()
    for error in resultado.get('errores', [])[:20]:
        messages.warning(request, error)

    if resultado.get('errores'):
        messages.error(request, 'La programación vigente se conservó; corrige el archivo e intenta de nuevo.')
        return redirect('consulta_aulas')

    for clave, etiqueta in (
        ('sedes_creadas', 'Sedes creadas'),
        ('edificios_creados', 'Edificios creados'),
        ('aulas_creadas', 'Aulas creadas con capacidad provisional de 30 personas'),
    ):
        if resultado.get(clave):
            messages.info(request, f"{etiqueta}: " + ', '.join(sorted(set(resultado[clave]))))

    messages.success(
        request,
        f"Importación completada: {resultado['total']} clases. El estado anterior quedó guardado en el historial.",
    )
    return redirect('consulta_aulas')


@roles_requeridos('ADMIN')
def historial_importaciones(request):
    institucion = _institucion_activa()
    if institucion is None:
        raise Http404('No hay institución activa.')
    importaciones = ImportacionProgramacion.objects.select_related('creado_por').all()
    return render(request, 'historial_importaciones.html', {
        'institucion_activa': institucion,
        'importaciones': importaciones,
    })


@roles_requeridos('ADMIN')
@require_POST
def restaurar_importacion(request, importacion_id):
    try:
        importacion = ImportacionProgramacion.objects.get(id=importacion_id)
    except ImportacionProgramacion.DoesNotExist as error:
        raise Http404('No se encontró la importación solicitada.') from error

    institucion = _institucion_activa()
    respaldo = importacion.respaldo_anterior
    try:
        clases_restauradas = clases_desde_respaldo(institucion, respaldo)
    except (KeyError, TypeError, ValueError):
        messages.error(request, 'El respaldo no tiene un formato válido y no se modificó la programación.')
        return redirect('historial_importaciones')

    with transaction.atomic():
        respaldo_actual = capturar_programacion(institucion)
        Clase.unfiltered.filter(institucion=institucion).delete()
        Clase.unfiltered.bulk_create(clases_restauradas)
        ImportacionProgramacion.unfiltered.create(
            institucion=institucion,
            archivo_nombre=f'Restauración de #{importacion.id}: {importacion.archivo_nombre}',
            tipo='RESTAURACION',
            creado_por=request.user,
            total_clases=len(clases_restauradas),
            respaldo_anterior=respaldo_actual,
        )

    messages.success(request, f'Se restauraron {len(clases_restauradas)} clases de la versión seleccionada.')
    return redirect('historial_importaciones')
