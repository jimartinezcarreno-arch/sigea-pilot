from proyectos.models import Aula, Clase


class AsignadorAulas:

    def buscar_aula_libre(
        self,
        institucion,
        edificio,
        dia,
        hora_inicio,
        hora_fin,
    ):

        aulas = Aula.unfiltered.filter(
            institucion=institucion,
            edificio=edificio
        ).order_by("nombre")

        for aula in aulas:

            conflicto = Clase.unfiltered.filter(
                institucion=institucion,
                aula=aula,
                dia_semana=dia,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            ).exists()

            if not conflicto:
                return aula

        return None