from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from .models import Edificio, Aula, Clase
from .tenant_utils import get_current_institucion

def mapa_interactivo(request):
    institucion = get_current_institucion()
    # Para el demo, tomaremos el primer edificio que tenga un plano
    edificios_con_plano = Edificio.objects.filter(plano_evacuacion__isnull=False)
    
    if request.GET.get('edificio_id'):
        edificio_seleccionado = get_object_or_404(edificios_con_plano, id=request.GET.get('edificio_id'))
    else:
        edificio_seleccionado = edificios_con_plano.first()

    return render(request, 'mapa_interactivo.html', {
        'edificios_con_plano': edificios_con_plano,
        'edificio_seleccionado': edificio_seleccionado,
    })

def api_estado_plano(request, edificio_id):
    """Devuelve JSON con las aulas de un edificio y su estado de ocupación actual."""
    edificio = get_object_or_404(Edificio, id=edificio_id)
    aulas = Aula.objects.filter(edificio=edificio, plano_x__isnull=False, plano_y__isnull=False)
    
    # Simular fecha y hora actual, o usar la real
    now = datetime.now()
    dia_actual = now.isoweekday() # 1: Lunes, 7: Domingo
    hora_actual = now.time()

    datos_aulas = []
    for aula in aulas:
        # Verificar si hay una clase en este momento
        clase_actual = Clase.objects.filter(
            aula=aula,
            dia_semana=dia_actual,
            hora_inicio__lte=hora_actual,
            hora_fin__gte=hora_actual
        ).first()
        
        datos_aulas.append({
            'id': aula.id,
            'nombre': aula.nombre,
            'x': aula.plano_x,
            'y': aula.plano_y,
            'tipo': aula.get_tipo_espacio_display(),
            'ocupada': clase_actual is not None,
            'clase_info': f"{clase_actual.asignatura} - Docente: {clase_actual.docente.nombre}" if clase_actual else "Libre"
        })
        
    plano_url = edificio.plano_evacuacion.url if edificio.plano_evacuacion else None
    
    return JsonResponse({
        'edificio': edificio.nombre,
        'plano_url': plano_url,
        'aulas': datos_aulas
    })
