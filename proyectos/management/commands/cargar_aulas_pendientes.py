from django.core.management.base import BaseCommand

from proyectos.models import (
    Institucion,
    Sede,
    Edificio,
    Aula,
)

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


class Command(BaseCommand):

    help = (
        "Carga las aulas nuevas detectadas en el Excel de Cúcuta y Ocaña "
        "(y el edificio Colegio del Rosario en Bucaramanga) con capacidad=30 "
        "y tipo 'Aula de Clase Ordinaria'. Dimensiones y recursos quedan "
        "vacíos para completarlos después desde el admin."
    )

    def handle(self, *args, **options):

        institucion = Institucion.objects.first()

        if not institucion:
            self.stdout.write(self.style.ERROR("No existe ninguna institución."))
            return

        self.stdout.write("")
        self.stdout.write("======================================")
        self.stdout.write(" CARGANDO AULAS NUEVAS (CUCUTA / OCAÑA / ROSARIO)")
        self.stdout.write("======================================")
        self.stdout.write("")

        total_sedes = 0
        total_edificios = 0
        total_aulas = 0

        for nombre_sede, edificios in FALTANTES.items():

            sede, creada = Sede.unfiltered.get_or_create(
                institucion=institucion,
                nombre=nombre_sede,
            )

            if creada:
                total_sedes += 1

            for nombre_edificio, aulas in edificios.items():

                edificio, creado = Edificio.unfiltered.get_or_create(
                    institucion=institucion,
                    sede=sede,
                    nombre=nombre_edificio,
                )

                if creado:
                    total_edificios += 1

                for nombre_aula in aulas:

                    aula, creada = Aula.unfiltered.get_or_create(
                        institucion=institucion,
                        edificio=edificio,
                        nombre=nombre_aula,
                        defaults={
                            "capacidad": 30,
                            "tipo_espacio": "AULA",
                        }
                    )

                    if creada:
                        total_aulas += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("AULAS NUEVAS CARGADAS"))
        self.stdout.write(f"Sedes creadas      : {total_sedes}")
        self.stdout.write(f"Edificios creados  : {total_edificios}")
        self.stdout.write(f"Aulas creadas      : {total_aulas}")
        self.stdout.write("")
        self.stdout.write("Ya puedes importar el Excel nuevo desde la interfaz.")