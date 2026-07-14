from django.core.management.base import BaseCommand

from proyectos.models import (
    Institucion,
    Sede,
    Edificio,
    Aula,
)

from proyectos.services.catalogo import CATALOGO


class Command(BaseCommand):

    help = "Carga el catálogo oficial de sedes, edificios y aulas."

    def handle(self, *args, **options):

        institucion = Institucion.objects.first()

        if not institucion:
            self.stdout.write(self.style.ERROR("No existe ninguna institución."))
            return

        self.stdout.write("")
        self.stdout.write("======================================")
        self.stdout.write(" CARGANDO CATÁLOGO OFICIAL")
        self.stdout.write("======================================")
        self.stdout.write("")

        total_sedes = 0
        total_edificios = 0
        total_aulas = 0

        for nombre_sede, edificios in CATALOGO.items():

            sede, creada = Sede.unfiltered.get_or_create(
                institucion=institucion,
                nombre=nombre_sede,
                defaults={
                    "direccion": ""
                }
            )

            if creada:
                total_sedes += 1

            for nombre_edificio, aulas in edificios.items():

                edificio, creado = Edificio.unfiltered.get_or_create(
                    institucion=institucion,
                    sede=sede,
                    nombre=nombre_edificio
                )

                if creado:
                    total_edificios += 1

                for nombre_aula, datos in aulas.items():

                    aula, creada = Aula.unfiltered.get_or_create(
                        institucion=institucion,
                        edificio=edificio,
                        nombre=nombre_aula,
                        defaults={
                            "capacidad": datos["capacidad"],
                            "tipo_espacio": datos["tipo"],
                        }
                    )

                    if creada:
                        total_aulas += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("CATÁLOGO CARGADO"))
        self.stdout.write(f"Sedes creadas      : {total_sedes}")
        self.stdout.write(f"Edificios creados  : {total_edificios}")
        self.stdout.write(f"Aulas creadas      : {total_aulas}")
        self.stdout.write("")