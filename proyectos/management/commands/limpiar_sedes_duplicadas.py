from django.core.management.base import BaseCommand

from proyectos.models import Institucion, Sede

# Los nombres correctos que deben quedar en el sistema.
NOMBRES_VALIDOS = {"CU Bucaramanga", "CU Cúcuta", "CU Ocaña"}


class Command(BaseCommand):

    help = (
        "Elimina sedes con nombres mal codificados (creadas por un error de "
        "consola de Windows), y solo si no tienen ningún edificio asociado, "
        "para no arriesgar datos reales."
    )

    def handle(self, *args, **options):

        institucion = Institucion.objects.first()

        if not institucion:
            self.stdout.write(self.style.ERROR("No existe ninguna institución."))
            return

        self.stdout.write("")
        self.stdout.write("======================================")
        self.stdout.write(" REVISANDO SEDES")
        self.stdout.write("======================================")
        self.stdout.write("")

        eliminadas = 0
        revisar_manual = 0

        for sede in Sede.unfiltered.filter(institucion=institucion):

            if sede.nombre in NOMBRES_VALIDOS:
                self.stdout.write(f"OK       : '{sede.nombre}'")
                continue

            total_edificios = sede.edificios.count()

            if total_edificios == 0:
                self.stdout.write(self.style.WARNING(
                    f"ELIMINANDO: '{sede.nombre}' (sin edificios asociados)"
                ))
                sede.delete()
                eliminadas += 1
            else:
                self.stdout.write(self.style.ERROR(
                    f"REVISAR MANUAL: '{sede.nombre}' tiene {total_edificios} "
                    "edificio(s) asociado(s). No se eliminó automáticamente."
                ))
                revisar_manual += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("LIMPIEZA TERMINADA"))
        self.stdout.write(f"Sedes eliminadas       : {eliminadas}")
        self.stdout.write(f"Sedes para revisar a mano: {revisar_manual}")
        self.stdout.write("")