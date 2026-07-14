"""
Carga las aulas nuevas detectadas en el Excel de Cúcuta y Ocaña
(y el edificio COLROS en Bucaramanga) con valores por defecto:
capacidad=30, tipo_espacio='AULA' (Aula de Clase Ordinaria).

Dimensiones y recursos quedan vacíos para completarlos después
desde el admin de Django cuando tengas esa información.

CÓMO CORRERLO (una sola vez, antes de importar el Excel nuevo):
    python manage.py shell < cargar_aulas_nuevas.py

Requiere que ya hayas reemplazado excel_importer.py con la versión
que incluye el mapeo de CU Cúcuta y CU Ocaña.
"""

from proyectos.models import Institucion, Sede, Edificio, Aula

institucion = Institucion.objects.first()
if institucion is None:
    raise SystemExit("No hay ninguna Institución creada todavía. Crea una antes de correr esto.")

# sede -> edificio -> [aulas]
FALTANTES = {
    "CU Cúcuta": {
        "COLSAL": [
            "B1B02", "C1C00", "C1C01", "B1B03", "C1C02", "C1C04",
            "C2C09", "C1C05", "B1B04", "B2B05", "C1C03", "B2B09", "C2C08",
        ],
        "CRCUC": ["403", "505", "404", "202", "405", "302", "304", "501", "502"],
    },
    "CU Ocaña": {
        "COLARC": [
            "UMDMAL103", "UMDMAL102", "UMDMAL104",
            "ASS10P1", "ASS8P1", "ASS1P1", "ASS11P1",
        ],
        "COLSAL": ["B1B02", "C2C11"],
    },
    "CU Bucaramanga": {
        "Colegio del Rosario": ["1", "B4", "B3", "B5", "3", "BIBLIOTECA", "9"],
        "San Juan Eudes": ["FarLab"],
    },
}

sedes_creadas = edificios_creados = aulas_creadas = 0

for nombre_sede, edificios in FALTANTES.items():
    sede, creada = Sede.unfiltered.get_or_create(
        institucion=institucion, nombre=nombre_sede
    )
    sedes_creadas += int(creada)

    for nombre_edificio, aulas in edificios.items():
        edificio, creada = Edificio.unfiltered.get_or_create(
            institucion=institucion, sede=sede, nombre=nombre_edificio
        )
        edificios_creados += int(creada)

        for nombre_aula in aulas:
            aula, creada = Aula.unfiltered.get_or_create(
                institucion=institucion,
                edificio=edificio,
                nombre=nombre_aula,
                defaults={"capacidad": 30, "tipo_espacio": "AULA"},
            )
            aulas_creadas += int(creada)

print(f"Sedes creadas: {sedes_creadas}")
print(f"Edificios creados: {edificios_creados}")
print(f"Aulas creadas: {aulas_creadas}")
print("Listo. Ahora puedes importar el Excel nuevo desde la interfaz.")