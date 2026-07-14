import logging
from datetime import datetime
from django.db import transaction
from django.core.exceptions import ValidationError
from openpyxl import load_workbook
from .asignador_aulas import AsignadorAulas

from proyectos.models import (
    ModalidadAcademica,
    PeriodoAcademico,
    MomentoAcademico,
    Sede,
    Edificio,
    Aula,
    Docente,
    Clase,
)

from .mappers import ExcelMapper
from .validators import ExcelValidator

logger = logging.getLogger(__name__)


class ExcelImporter:

    MAPA_SEDES = {
        "BUC": "CU Bucaramanga",
        "S": "CU Bucaramanga",
        "CUC": "CU Cúcuta",
        "OCA": "CU Ocaña",
    }

    MAPA_EDIFICIOS = {
        "DJCB": "Diego Jaramillo",
        "SJEB": "San Juan Eudes",
        "FARLAB": "Biblioteca",
        "COLROS": "Colegio del Rosario",
    }

    MAPA_AULAS = {

        "SAL BIBLIO": "FarLab",

        "FARLAB": "FarLab",

        "MAKERLAB": "FarLab",

        "200": "201",

    }

    DIAS = {
        "lunes": 1,
        "martes": 2,
        "miercoles": 3,
        "jueves": 4,
        "viernes": 5,
        "sabado": 6,
        "domingo": 7,
    }

    def __init__(self, archivo, institucion):

        self.archivo = archivo
        self.institucion = institucion

        self.errores = []
        self.total = 0
        self.sedes_creadas = []
        self.edificios_creados = []

    def convertir_hora(self, valor):

        if valor is None:
            return None

        valor = str(valor).replace(".0", "").strip()

        while len(valor) < 4:
            valor = "0" + valor

        return datetime.strptime(
            valor,
            "%H%M"
        ).time()

    @transaction.atomic
    def importar(self):

        logger.info("SIGEA IMPORTADOR: Inicio de importación")

        workbook = load_workbook(
            self.archivo,
            data_only=True
        )

        hoja = workbook.active

        cabeceras = [

            str(c.value).strip().upper()

            if c.value else ""

            for c in hoja[1]

        ]

        indices, faltantes = ExcelMapper.obtener_indices(
            cabeceras
        )

        errores = ExcelValidator.validar(
            indices
        )

        if errores:

            return {

                "total": 0,

                "errores": errores,

            }

        modalidad, _ = ModalidadAcademica.unfiltered.get_or_create(

            institucion=self.institucion,

            nombre="PRESENCIAL",

        )

        codigo_periodo = "202610"

        if indices["periodo"] is not None:

            fila = next(

                hoja.iter_rows(

                    min_row=2,

                    max_row=2,

                    values_only=True,

                )

            )

            codigo_periodo = str(

                fila[indices["periodo"]]

            ).strip()

        periodo, _ = PeriodoAcademico.unfiltered.get_or_create(

            institucion=self.institucion,

            codigo_institucional=codigo_periodo,

            defaults={

                "modalidad": modalidad,

                "nombre": codigo_periodo,

                "fecha_inicio": datetime(
                    2026,
                    1,
                    1
                ).date(),

                "fecha_fin": datetime(
                    2026,
                    12,
                    31
                ).date(),

            }

                )

        momento, _ = MomentoAcademico.objects.get_or_create(

            periodo=periodo,

            nombre="Periodo Completo",

            defaults={

                "fecha_inicio": periodo.fecha_inicio,

                "fecha_fin": periodo.fecha_fin,

            }

        )


        Clase.unfiltered.filter(
            institucion=self.institucion
        ).delete()

        logger.info("Importando clases...")

        dias = {
            "lunes": 1,
            "martes": 2,
            "miercoles": 3,
            "jueves": 4,
            "viernes": 5,
            "sabado": 6,
            "domingo": 7,
        }

        total = 0

        asignador = AsignadorAulas()

        for fila in hoja.iter_rows(
            min_row=2,
            values_only=True,
        ):

            if not fila:
                continue

            nombre_sede = str(
                fila[indices["sede"]] or ""
            ).strip().upper()

            nombre_sede = self.MAPA_SEDES.get(
                nombre_sede,
                nombre_sede
            )

            sede = Sede.unfiltered.filter(
                institucion=self.institucion,
                nombre__iexact=nombre_sede
            ).first()

            if not sede:

                if not nombre_sede:
                    self.errores.append(
                        "Fila sin sede: la columna SEDE/CAMPUS viene vacía."
                    )
                    continue

                sede = Sede.unfiltered.create(
                    institucion=self.institucion,
                    nombre=nombre_sede,
                )

                self.sedes_creadas.append(nombre_sede)

            # -----------------------------
            # EDIFICIO
            # -----------------------------

            nombre_edificio = str(
                fila[indices["edificio"]] or ""
            ).strip().upper()

            nombre_edificio = self.MAPA_EDIFICIOS.get(
                nombre_edificio,
                nombre_edificio
            )

            if nombre_edificio in ("VIRTU", "SINCR", ""):

                edificio, _ = Edificio.unfiltered.get_or_create(
                    institucion=self.institucion,
                    sede=sede,
                    nombre="Virtual",
                )

                aula, _ = Aula.unfiltered.get_or_create(
                    institucion=self.institucion,
                    edificio=edificio,
                    nombre="VIRTUAL",
                    defaults={
                        "capacidad": 999,
                        "tipo_espacio": "VIRTUAL",
                    }
                )

            else:

                edificio = Edificio.unfiltered.filter(
                    institucion=self.institucion,
                    sede=sede,
                    nombre__iexact=nombre_edificio
                ).first()

                if not edificio:

                    if not nombre_edificio:
                        self.errores.append(
                            f"Fila sin edificio (sede: {sede.nombre}): la "
                            "columna EDIFICIO/BLOQUE viene vacía."
                        )
                        continue

                    edificio = Edificio.unfiltered.create(
                        institucion=self.institucion,
                        sede=sede,
                        nombre=nombre_edificio,
                    )

                    self.edificios_creados.append(
                        f"{nombre_edificio} ({sede.nombre})"
                    )

                # -----------------------------
                # AULA
                # -----------------------------

                nombre_aula = str(
                    fila[indices["aula"]] or ""
                ).strip().upper()

                nombre_aula = self.MAPA_AULAS.get(
                    nombre_aula,
                    nombre_aula
                )

                aula = Aula.unfiltered.filter(
                    institucion=self.institucion,
                    edificio=edificio,
                    nombre__iexact=nombre_aula
                ).first()

                if not aula:

                    aula = Aula.unfiltered.filter(
                        institucion=self.institucion,
                        nombre__iexact=nombre_aula
                    ).first()

                if not aula:
                    self.errores.append(
                        f"Aula no encontrada: {nombre_aula}"
                    )
                    continue

            # -----------------------------
            # DOCENTE
            # -----------------------------

            nombre_docente = str(
                fila[indices["docente"]] or "SIN DOCENTE"
            ).strip()

            docente, _ = Docente.unfiltered.get_or_create(
                institucion=self.institucion,
                nombre=nombre_docente,
                defaults={
                    "identificacion": "",
                    "email": "",
                }
            )

            hora_inicio = self.convertir_hora(
                fila[indices["hora_inicio"]]
            )

            hora_fin = self.convertir_hora(
                fila[indices["hora_fin"]]
            )

            asignatura = str(
                fila[indices["asignatura"]] or ""
            ).strip()

            nrc = str(
                fila[indices["nrc"]] or ""
            ).strip()

            for nombre_dia, numero_dia in dias.items():

                indice = indices[nombre_dia]

                if indice is None:
                    continue

                if fila[indice] in (None, ""):
                    continue

                try:

                    Clase.unfiltered.create(

                        institucion=self.institucion,

                        docente=docente,

                        aula=aula,

                        periodo=periodo,

                        momento=momento,

                        asignatura=asignatura,

                        nrc=nrc,

                        dia_semana=numero_dia,

                        hora_inicio=hora_inicio,

                        hora_fin=hora_fin,

                    )

                    total += 1

                except (ValidationError, Exception) as e:

                    self.errores.append(
                        f"NRC {nrc}: {str(e)}"
                    )


        logger.info(f"Clases creadas: {total}")
        logger.info(f"Errores: {len(self.errores)}")
        if self.errores:
            logger.warning(f"Primeros errores: {self.errores[:10]}")

        return {

            "total": total,

            "errores": self.errores,

            "sedes_creadas": self.sedes_creadas,

            "edificios_creados": self.edificios_creados,

        }