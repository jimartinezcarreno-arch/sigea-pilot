from io import BytesIO

from django.contrib import messages
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from .models import Clase, ImportacionProgramacion, Institucion
from .permissions import roles_requeridos
from .services.excel_importer import ExcelImporter
from .services.programacion_backup import capturar_programacion, clases_desde_respaldo
from .tenant_utils import get_current_institucion


def _institucion_activa():
    return get_current_institucion() or Institucion.objects.first()


@roles_requeridos('ADMIN', 'PROGRAMADOR', 'CONSULTA')
def descargar_plantilla_programacion(request):
    libro = Workbook()
    hoja = libro.active
    hoja.title = 'Programación'
    encabezados = [
        'PERIODO', 'NRC', 'TITULO', 'NOMBRE_DOCENTE', 'SEDE', 'EDIFICIO',
        'SALON', 'HI', 'HF', 'L', 'M', 'I', 'J', 'V', 'S', 'D',
    ]
    hoja.append(encabezados)
    for celda in hoja[1]:
        celda.font = Font(bold=True, color='FFFFFF')
        celda.fill = PatternFill('solid', fgColor='2563EB')
    hoja.freeze_panes = 'A2'
    for columna in hoja.columns:
        hoja.column_dimensions[columna[0].column_letter].width = 19

    instrucciones = libro.create_sheet('Instrucciones')
    instrucciones.append(['Guía de importación SIGEA'])
    instrucciones['A1'].font = Font(bold=True, size=14, color='FFFFFF')
    instrucciones['A1'].fill = PatternFill('solid', fgColor='1D4ED8')
    instrucciones.merge_cells('A1:B1')
    instrucciones.append(['Campo', 'Uso'])
    instrucciones.append(['PERIODO', 'Código del periodo académico, por ejemplo 202610.'])
    instrucciones.append(['NRC', 'Identificador único de la clase.'])
    instrucciones.append(['TITULO', 'Nombre de la asignatura.'])
    instrucciones.append(['NOMBRE_DOCENTE', 'Nombre completo del docente.'])
    instrucciones.append(['SEDE / EDIFICIO / SALON', 'Ubicación física de la clase. SIGEA crea espacios nuevos con capacidad provisional.'])
    instrucciones.append(['HI / HF', 'Hora de inicio y fin en formato HHMM: por ejemplo 0830 y 1000.'])
    instrucciones.append(['L, M, I, J, V, S, D', 'Marca con X los días de clase: lunes a domingo.'])
    instrucciones.append(['Importante', 'Elimina cualquier fila de ejemplo y conserva exactamente los encabezados de la primera hoja.'])
    instrucciones.column_dimensions['A'].width = 34
    instrucciones.column_dimensions['B'].width = 100
    for celda in instrucciones[2]:
        celda.font = Font(bold=True)

    contenido = BytesIO()
    libro.save(contenido)
    respuesta = HttpResponse(
        contenido.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    respuesta['Content-Disposition'] = 'attachment; filename="plantilla_programacion_sigea.xlsx"'
    return respuesta


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
