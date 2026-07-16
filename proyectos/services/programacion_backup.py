from datetime import time

from proyectos.models import Clase


CAMPOS_RESPALDO = (
    'docente_id',
    'aula_id',
    'periodo_id',
    'momento_id',
    'asignatura',
    'nrc',
    'dia_semana',
    'hora_inicio',
    'hora_fin',
)


def capturar_programacion(institucion):
    """Serializa las clases de una institución usando solamente datos restaurables."""
    clases = Clase.unfiltered.filter(institucion=institucion).values(*CAMPOS_RESPALDO)
    respaldo = []
    for clase in clases:
        respaldo.append({
            **clase,
            'hora_inicio': clase['hora_inicio'].isoformat(),
            'hora_fin': clase['hora_fin'].isoformat(),
        })
    return respaldo


def clases_desde_respaldo(institucion, respaldo):
    """Reconstruye instancias de Clase sin guardar cambios parciales."""
    clases = []
    for fila in respaldo:
        clases.append(Clase(
            institucion=institucion,
            docente_id=fila['docente_id'],
            aula_id=fila['aula_id'],
            periodo_id=fila['periodo_id'],
            momento_id=fila['momento_id'],
            asignatura=fila['asignatura'],
            nrc=fila['nrc'],
            dia_semana=fila['dia_semana'],
            hora_inicio=time.fromisoformat(fila['hora_inicio']),
            hora_fin=time.fromisoformat(fila['hora_fin']),
        ))
    return clases
