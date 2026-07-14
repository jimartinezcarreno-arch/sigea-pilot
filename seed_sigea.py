import os
import django
from datetime import time, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planimetria.settings')
django.setup()

from proyectos.models import Institucion, Aula, Sede, Edificio, Docente, PeriodoAcademico

def seed():
    # 1. Clear database
    print("Limpiando base de datos...")
    Institucion.objects.all().delete()

    # 2. Create Colegio Mayor
    inst1 = Institucion.objects.create(
        nombre="COLEGIO MAYOR DE ANTIOQUIA",
        subdominio="colegio",
        hora_inicio_jornada=time(6, 0),
        hora_fin_jornada=time(22, 0),
        activo=True
    )

    # 3. Create Academia Técnica
    inst2 = Institucion.objects.create(
        nombre="ACADEMIA TÉCNICA INDUSTRIAL",
        subdominio="tecnico",
        hora_inicio_jornada=time(7, 0),
        hora_fin_jornada=time(18, 0),
        activo=True
    )

    # 4. Add Periodos Académicos
    PeriodoAcademico.objects.create(
        institucion=inst1,
        nombre="2026-1",
        fecha_inicio=date(2026, 2, 1),
        fecha_fin=date(2026, 6, 30),
        fecha_inicio_rt1=date(2026, 2, 1),
        fecha_fin_rt1=date(2026, 3, 27),
        fecha_inicio_rt2=date(2026, 3, 28),
        fecha_fin_rt2=date(2026, 6, 30)
    )
    
    PeriodoAcademico.objects.create(
        institucion=inst2,
        nombre="2026-1",
        fecha_inicio=date(2026, 2, 1),
        fecha_fin=date(2026, 6, 30),
        fecha_inicio_rt1=date(2026, 2, 1),
        fecha_fin_rt1=date(2026, 3, 27),
        fecha_inicio_rt2=date(2026, 3, 28),
        fecha_fin_rt2=date(2026, 6, 30)
    )

    # 5. Create some default classrooms for the map and autocomplete
    sede_c = Sede.objects.create(nombre="SEDE CENTRAL COLEGIO", institucion=inst1)
    edf_a = Edificio.objects.create(nombre="EDIFICIO A", sede=sede_c, institucion=inst1)
    
    Aula.objects.create(nombre="AULA 101", edificio=edf_a, institucion=inst1, capacidad=40, tipo_espacio="AULA", recursos="Proyector, Aire Acondicionado")
    Aula.objects.create(nombre="AULA 102", edificio=edf_a, institucion=inst1, capacidad=40, tipo_espacio="AULA", recursos="Proyector")
    Aula.objects.create(nombre="LAB-301", edificio=edf_a, institucion=inst1, capacidad=35, tipo_espacio="LABORATORIO", recursos="Computadores (35), Extractor")
    Aula.objects.create(nombre="AUDITORIO A", edificio=edf_a, institucion=inst1, capacidad=100, tipo_espacio="AUDITORIO", recursos="Sonido Envolvente, Proyector HD")

    print("Base de datos inicializada con exito:")
    print("   - Institucion 1: COLEGIO MAYOR DE ANTIOQUIA (subdominio: colegio)")
    print("   - Institucion 2: ACADEMIA TECNICA INDUSTRIAL (subdominio: tecnico)")
    print("   - Aulas base creadas para el mapa del Colegio Mayor (AULA 101, AULA 102, LAB-301, AUDITORIO A)")

if __name__ == '__main__':
    seed()
