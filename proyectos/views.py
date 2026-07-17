from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, time
import json
from .tenant_utils import get_current_institucion
from .services.excel_importer import ExcelImporter
import openpyxl

from .models import (
    Sede,
    Edificio,
    Aula,
    Clase,
    PeriodoAcademico,
    MomentoAcademico,
    Docente,
    Institucion,
    ModalidadAcademica
)


@login_required
def dashboard_modulos(request):
    """Página de selección de módulos después del login"""
    institucion = get_current_institucion()
    context = {
        'institucion': institucion,
    }
    return render(request, 'dashboard_modulos.html', context)

# -------------------------------
# CONSULTA DE AULAS DISPONIBLES
# -------------------------------
def aulas_disponibles(request):

    sedes = Sede.objects.all()

    edificios = Edificio.objects.none()

    aulas_select = Aula.objects.none()

    sede_id = request.GET.get("sede")

    edificio_id = request.GET.get("edificio")

    aula_id = request.GET.get("aula")

    docente_id = request.GET.get("docente")

    hora_buscada_str = request.GET.get("hora") or "18:30"

    # Filtrar docentes por sede seleccionada
    if sede_id:
        docentes_select = Docente.objects.filter(
            clases__aula__edificio__sede_id=sede_id
        ).distinct()
    else:
        docentes_select = Docente.objects.all()

    if sede_id:

        edificios = (
            Edificio.objects
            .filter(
                sede_id=sede_id
            )
            .order_by(
                "nombre"
            )
        )

    if edificio_id:

        aulas_select = (
            Aula.objects
            .filter(
                edificio_id=edificio_id
            )
            .order_by(
                "nombre"
            )
        )

    try:

        hora_consulta = datetime.strptime(
            hora_buscada_str,
            "%H:%M"
        ).time()

    except ValueError:

        hora_consulta = time(
            18,
            30
        )

    aulas_query = Aula.objects.all()

    if sede_id:

        aulas_query = aulas_query.filter(
            edificio__sede_id=sede_id
        )

    if edificio_id:

        aulas_query = aulas_query.filter(
            edificio_id=edificio_id
        )

    if aula_id:

        aulas_query = aulas_query.filter(
            id=aula_id
        )

    if docente_id:

        aulas_query = aulas_query.filter(
            clases__docente_id=docente_id
        ).distinct()

    # Optimize N+1 query problem with prefetch_related
    aulas_query = aulas_query.prefetch_related('clases__docente')

    resultado = []

    hora_actual = datetime.now().time()
    dia_actual = datetime.now().weekday() + 1  # Django usa 1=Lunes, 7=Domingo

    libres_count = 0
    ocupadas_count = 0

    # Logging para diagnóstico
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"=== DIAGNÓSTICO AULAS DISPONIBLES ===")
    logger.info(f"Total aulas en query: {aulas_query.count()}")
    logger.info(f"Hora consulta: {hora_consulta}")
    logger.info(f"Parámetros: sede_id={sede_id}, edificio_id={edificio_id}, aula_id={aula_id}, docente_id={docente_id}")

    for aula in aulas_query:

        clases_aula = Clase.objects.filter(
            aula=aula
        )

        if docente_id:

            clases_aula = clases_aula.filter(
                docente_id=docente_id
            )

        clases_aula = clases_aula.order_by("dia_semana", "hora_inicio")

        # Log primeras 3 aulas y sus clases
        if len(resultado) < 3:
            logger.info(f"Aula: {aula.nombre} (ID: {aula.id}) - Total clases: {clases_aula.count()}")
            if clases_aula.count() > 0:
                for c in clases_aula[:3]:
                    logger.info(f"  Clase: {c.asignatura} - Día: {c.dia_semana} - {c.hora_inicio}-{c.hora_fin}")

        clase_en_curso = None

        for c in clases_aula:

            if c.hora_inicio <= hora_consulta <= c.hora_fin:

                clase_en_curso = c

                break

        # Calcular próxima clase y tiempo libre
        proxima_clase = None
        tiempo_libre_minutos = None
        
        if clase_en_curso:
            # Si está ocupada, calcular tiempo hasta que termine
            fin_clase = datetime.combine(datetime.today(), clase_en_curso.hora_fin)
            ahora = datetime.combine(datetime.today(), hora_actual)
            tiempo_restante = (fin_clase - ahora).total_seconds() / 60
            if tiempo_restante > 0:
                tiempo_libre_minutos = int(tiempo_restante)
        else:
            # Si está libre, buscar próxima clase hoy
            clases_hoy = clases_aula.filter(dia_semana=dia_actual).filter(hora_inicio__gt=hora_actual).order_by('hora_inicio').first()
            if clases_hoy:
                proxima_clase = clases_hoy
                inicio_proxima = datetime.combine(datetime.today(), clases_hoy.hora_inicio)
                ahora = datetime.combine(datetime.today(), hora_actual)
                tiempo_libre = (inicio_proxima - ahora).total_seconds() / 60
                if tiempo_libre > 0:
                    tiempo_libre_minutos = int(tiempo_libre)

        estado = (
            "OCUPADA"
            if clase_en_curso
            else "DISPONIBLE"
        )

        if estado == "DISPONIBLE":
            libres_count += 1

        # Log estado de primeras 3 aulas
        if len(resultado) < 3:
            logger.info(f"  Estado: {estado} - Clase en curso: {clase_en_curso.asignatura if clase_en_curso else 'Ninguna'}")

        if estado == "OCUPADA":
            ocupadas_count += 1

        resultado.append({
            "aula": aula,
            "estado": estado,
            "materia_actual": (
                clase_en_curso.asignatura
                if clase_en_curso
                else None
            ),

            "docente_actual": (
                clase_en_curso.docente.nombre
                if clase_en_curso
                else None
            ),

            "horarios_ocupados": clases_aula,

            "proxima_clase": proxima_clase,

            "tiempo_libre_minutos": tiempo_libre_minutos,

        })

    # -------------------------------
    # ESTADÍSTICAS FILTRADAS
    # -------------------------------

    total_aulas = aulas_query.count()

    total_docentes = Docente.objects.count()

    # Total de clases asociadas a las aulas y docente actualmente filtrados
    clases_filtradas = Clase.objects.filter(aula__in=aulas_query)
    if docente_id:
        clases_filtradas = clases_filtradas.filter(docente_id=docente_id)
    total_clases = clases_filtradas.count()

    aulas_libres = libres_count
    aulas_ocupadas = ocupadas_count

    # Logging final para diagnóstico
    logger.info(f"=== RESUMEN DIAGNÓSTICO ===")
    logger.info(f"Total aulas procesadas: {total_aulas}")
    logger.info(f"Total clases filtradas: {total_clases}")
    logger.info(f"Aulas libres: {aulas_libres}")
    logger.info(f"Aulas ocupadas: {aulas_ocupadas}")
    logger.info(f"Total docentes: {total_docentes}")
    logger.info(f"Resultado length: {len(resultado)}")

    context = {

        "sedes": sedes,

        "edificios": edificios,

        "aulas_select": aulas_select,

        "docentes_select": docentes_select,

        "resultado": resultado,

        "sede_id": sede_id,

        "edificio_id": edificio_id,

        "aula_id": aula_id,

        "docente_seleccionado": docente_id,

        "hora": hora_buscada_str,

        "institucion_activa": Institucion.objects.first(),

        "total_aulas": total_aulas,

        "total_docentes": total_docentes,

        "total_clases": total_clases,

        "aulas_libres": aulas_libres,

        "aulas_ocupadas": aulas_ocupadas,

        "libres_count": libres_count,

        "ocupadas_count": ocupadas_count,

    }

    return render(
        request,
        "consulta_dashboard.html",
        context
    )

# -------------------------------
# IMPORTACIÓN DE EXCEL
# -------------------------------
def subir_excel(request):
    """
    Carga la programación académica desde un archivo Excel.
    Toda la lógica del proceso vive en ExcelImporter.
    """

    if request.method != "POST":
        return redirect("consulta_aulas")

    archivo = request.FILES.get("archivo_excel")

    if not archivo:
        messages.error(request, "Debe seleccionar un archivo Excel.")
        return redirect("consulta_aulas")

    # Intentar obtener la institución activa
    institucion = get_current_institucion()

    # Durante el desarrollo usar la primera registrada
    if institucion is None:
        institucion = Institucion.objects.first()

    # Si no existe ninguna, crear una
    if institucion is None:
        institucion = Institucion.objects.create(
            nombre="SIGEA",
            subdominio="localhost",
            hora_inicio_jornada=time(6, 0),
            hora_fin_jornada=time(22, 0),
            activo=True,
        )

    servicio = ExcelImporter(
        archivo=archivo,
        institucion=institucion
    )

    resultado = servicio.importar()

    if resultado["errores"]:
        for error in resultado["errores"][:20]:
            messages.warning(request, error)

    if resultado.get("sedes_creadas"):
        messages.info(
            request,
            "Sedes nuevas detectadas y creadas automáticamente: "
            + ", ".join(sorted(set(resultado["sedes_creadas"])))
        )

    if resultado.get("edificios_creados"):
        messages.info(
            request,
            "Edificios nuevos detectados y creados automáticamente: "
            + ", ".join(sorted(set(resultado["edificios_creados"])))
        )

    if resultado.get("aulas_creadas"):
        messages.info(
            request,
            "Aulas nuevas creadas con capacidad provisional de 30 personas: "
            + ", ".join(sorted(set(resultado["aulas_creadas"])))
        )

    messages.success(
        request,
        f"Importación finalizada. Se cargaron {resultado['total']} clases."
    )

    return redirect("consulta_aulas")

# -------------------------------
# MAPA INTERACTIVO
# -------------------------------
def mapa_interactivo(request):
    institucion = Institucion.objects.first()
    return render(request, 'mapa_interactivo.html', {"institucion_activa": institucion})


# -------------------------------
# SELECTORES AJAX
# -------------------------------

def obtener_edificios(request):
    sede_id = request.GET.get("sede_id")

    edificios = (
        Edificio.objects
        .filter(sede_id=sede_id)
        .order_by("nombre")
    )

    return JsonResponse(
        [
            {
                "id": e.id,
                "nombre": e.nombre,
            }
            for e in edificios
        ],
        safe=False,
    )


def obtener_aulas(request):
    edificio_id = request.GET.get("edificio_id")

    aulas = (
        Aula.objects
        .filter(edificio_id=edificio_id)
        .order_by("nombre")
    )

    return JsonResponse(
        [
            {
                "id": a.id,
                "nombre": a.nombre,
            }
            for a in aulas
        ],
        safe=False,
    )


# -------------------------------
# REPORTE DE CONFLICTOS
# -------------------------------
def reporte_conflictos(request):
    institucion = Institucion.objects.first()
    conflictos = []
    clases = Clase.objects.select_related('aula', 'docente', 'aula__edificio').all()

    clases_revisadas = set()

    for clase in clases:
        if clase.id in clases_revisadas:
            continue

        choques = Clase.objects.filter(
            aula=clase.aula,
            dia_semana=clase.dia_semana,
            hora_inicio__lt=clase.hora_fin,
            hora_fin__gt=clase.hora_inicio
        ).exclude(id=clase.id).select_related('docente')

        if choques.exists():
            # Marcar todas las clases involucradas como revisadas
            for choque in choques:
                clases_revisadas.add(choque.id)
            clases_revisadas.add(clase.id)

            # Buscar aula alternativa que esté libre en ese horario y día
            aulas_ocupadas_ids = Clase.objects.filter(
                dia_semana=clase.dia_semana,
                hora_inicio__lt=clase.hora_fin,
                hora_fin__gt=clase.hora_inicio
            ).values_list('aula_id', flat=True)

            aula_sugerida = Aula.objects.exclude(
                id__in=aulas_ocupadas_ids
            ).exclude(id=clase.aula.id).first()

            conflictos.append({
                "clase": clase,
                "conflictos": choques,
                "aula_sugerida": aula_sugerida
            })

    return render(request, "reporte_conflictos.html", {
        "conflictos": conflictos,
        "total_conflictos": len(conflictos),
        "institucion_activa": institucion
    })


# -------------------------------
# REASIGNACIÓN DE AULA ALTERNATIVA
# -------------------------------
def asignar_aula_alternativa(request, clase_id, aula_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        clase = Clase.objects.get(id=clase_id)
        aula = Aula.objects.get(id=aula_id)

        aula_ocupada = Clase.objects.filter(
            aula=aula,
            dia_semana=clase.dia_semana,
            hora_inicio__lt=clase.hora_fin,
            hora_fin__gt=clase.hora_inicio,
        ).exclude(id=clase.id).exists()
        if aula_ocupada:
            messages.error(request, "El aula sugerida ya no estÃ¡ disponible en ese horario.")
            return redirect("reporte_conflictos")

        clase.aula = aula
        clase.save()
        messages.success(request, f"Aula reasignada a {aula.nombre} correctamente.")
    except Exception as e:
        messages.error(request, f"Error al reasignar aula: {str(e)}")
    return redirect("reporte_conflictos")


# -------------------------------
# AGENDA DOCENTE
# -------------------------------
def agenda_docente(request, docente_id):
    docente = Docente.objects.get(id=docente_id)
    clases = Clase.objects.filter(docente=docente).select_related('aula__edificio').order_by('dia_semana', 'hora_inicio')
    todos_docentes = Docente.objects.all()
    
    # Agrupar clases por día de la semana
    DIAS_SEMANA = {
        1: 'Lunes',
        2: 'Martes', 
        3: 'Miércoles',
        4: 'Jueves',
        5: 'Viernes',
        6: 'Sábado',
        7: 'Domingo'
    }
    
    clases_por_dia = {}
    for dia_num, dia_nombre in DIAS_SEMANA.items():
        clases_dia = clases.filter(dia_semana=dia_num).order_by('hora_inicio')
        if clases_dia.exists():
            clases_por_dia[dia_nombre] = clases_dia

    # Formato para FullCalendar
    eventos = []
    for c in clases:
        eventos.append({
            "title": f"{c.asignatura} ({c.nrc})",
            # FullCalendar usa 0 para domingo y 1 para lunes.
            "daysOfWeek": [c.dia_semana % 7],
            "startTime": str(c.hora_inicio),
            "endTime": str(c.hora_fin),
            "extendedProps": {
                "aula": c.aula.nombre,
                "edificio": c.aula.edificio.nombre,
                "nrc": c.nrc,
            },
        })

    return render(request, "agenda_docente.html", {
        "docente": docente,
        "eventos": eventos,
        "clases_por_dia": clases_por_dia,
        "todos_docentes": todos_docentes
    })


# -------------------------------
# DASHBOARD DE REPORTES
# -------------------------------
def dashboard_reportes(request):
    from django.db.models import Count, Avg, Q
    from datetime import datetime, time as time_class
    
    institucion = Institucion.objects.first()

    # Estadísticas de ocupación de aulas
    aulas = Aula.objects.all()
    ocupacion_labels = []
    ocupacion_data = []
    
    for aula in aulas:
        total_clases = Clase.objects.filter(aula=aula).count()
        # Calcular porcentaje de ocupación basado en horas disponibles
        # Asumiendo 8 horas diarias de uso potencial (8am-4pm) x 5 días = 40 horas semanales
        horas_usadas = 0
        clases_aula = Clase.objects.filter(aula=aula)
        for clase in clases_aula:
            inicio = datetime.combine(datetime.today(), clase.hora_inicio)
            fin = datetime.combine(datetime.today(), clase.hora_fin)
            horas_usadas += (fin - inicio).total_seconds() / 3600
        
        porcentaje = min(100, (horas_usadas / 40) * 100) if total_clases > 0 else 0
        ocupacion_labels.append(aula.nombre)
        ocupacion_data.append(round(porcentaje, 1))

    # Ranking de docentes por horas de clase
    docentes = Docente.objects.all()
    docentes_data = []
    
    for d in docentes:
        horas = sum([
            (datetime.combine(datetime.today(), c.hora_fin) - datetime.combine(datetime.today(), c.hora_inicio)).total_seconds() / 3600
            for c in Clase.objects.filter(docente=d)
        ])
        docentes_data.append({
            'nombre': d.nombre,
            'horas': round(horas, 1),
            'clases': Clase.objects.filter(docente=d).count()
        })
    
    # El grÃ¡fico conserva un resumen legible; la tabla muestra todos los docentes.
    docentes_data = sorted(docentes_data, key=lambda x: x['horas'], reverse=True)
    top_docentes = docentes_data[:10]
    docentes_labels = [d['nombre'] for d in top_docentes]
    docentes_horas = [d['horas'] for d in top_docentes]

    # Ranking de aulas por utilización
    espacios_data = []
    for aula in aulas:
        total_clases = Clase.objects.filter(aula=aula).count()
        espacios_data.append({
            'nombre': aula.nombre,
            'edificio': aula.edificio.nombre,
            'clases': total_clases,
            'capacidad': aula.capacidad
        })
    
    # Ordenar aulas por número de clases (top 10)
    espacios_data = sorted(espacios_data, key=lambda x: x['clases'], reverse=True)[:10]
    espacios_labels = [e['nombre'] for e in espacios_data]
    espacios_clases = [e['clases'] for e in espacios_data]

    # Estadísticas generales
    total_aulas = Aula.objects.count()
    total_docentes = Docente.objects.count()
    total_clases = Clase.objects.count()
    
    # Calcular ocupación promedio del sistema
    if total_aulas > 0:
        ocupacion_promedio = sum(ocupacion_data) / len(ocupacion_data)
    else:
        ocupacion_promedio = 0

    context = {
        "institucion_activa": institucion,
        "ocupacion_labels": ocupacion_labels,
        "ocupacion_data": ocupacion_data,
        "docentes_labels": docentes_labels,
        "docentes_horas": docentes_horas,
        "docentes_data": docentes_data,
        "espacios_labels": espacios_labels,
        "espacios_clases": espacios_clases,
        "espacios_data": espacios_data,
        "total_aulas": total_aulas,
        "total_docentes": total_docentes,
        "total_clases": total_clases,
        "ocupacion_promedio": round(ocupacion_promedio, 1),
        "ocupacion_labels_json": json.dumps(ocupacion_labels),
        "ocupacion_data_json": json.dumps(ocupacion_data),
        "docentes_labels_json": json.dumps(docentes_labels),
        "docentes_horas_json": json.dumps(docentes_horas),
        "espacios_labels_json": json.dumps(espacios_labels),
        "espacios_clases_json": json.dumps(espacios_clases),
    }
    return render(request, "dashboard_reportes.html", context)
