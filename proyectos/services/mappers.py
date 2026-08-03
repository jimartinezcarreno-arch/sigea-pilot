class ExcelMapper:

    """
    Traduce las columnas del Excel al modelo interno de SIGEA.
    """

    COLUMNAS = {

        "periodo": [
            "PERIODO",
            "PERÍODO",
            "PERIODO_ACADEMICO",
            "PERÍODO_ACADÉMICO",
        ],

        # Esta columna es opcional. Algunas instituciones incluyen registros
        # inactivos en la misma hoja de planeación y no deben ocupar un aula.
        "estado_nrc": [
            "ESTADO_NRC",
            "ESTADO NRC",
            "ESTADO",
        ],

        "nrc": [
            "NRC",
            "ID_CLASE",
            "IDENTIFICADOR_CLASE",
            "CODIGO_CLASE",
            "CÓDIGO_CLASE",
        ],

        "asignatura": [
            "TITULO",
            "ASIGNATURA",
            "MATERIA",
            "CURSO",
            "NOMBRE_ASIGNATURA",
        ],

        "docente": [
            "NOMBRE_DOCENTE",
            "DOCENTE",
            "PROFESOR",
            "INSTRUCTOR",
        ],

        "sede": [
            "SEDE",
            "CAMPUS",
        ],

        "edificio": [
            "EDIFICIO",
            "BLOQUE",
        ],

        "aula": [
            "SALON",
            "SALÓN",
            "AULA",
            "ESPACIO",
            "ESPACIO_ACADEMICO",
            "ESPACIO_ACADÉMICO",
        ],

        "hora_inicio": [
            "HI",
            "HORA INICIO",
            "HORA_INICIO",
            "INICIO",
        ],

        "hora_fin": [
            "HF",
            "HORA FIN",
            "HORA_FIN",
            "HORA_FINAL",
            "FIN",
        ],

        "lunes": ["L", "LUN", "LUNES"],
        "martes": ["M", "MAR", "MARTES"],
        "miercoles": ["I", "MIE", "MIÉ", "MIERCOLES", "MIÉRCOLES"],
        "jueves": ["J", "JUE", "JUEVES"],
        "viernes": ["V", "VIE", "VIERNES"],
        "sabado": ["S", "SAB", "SÁB", "SABADO", "SÁBADO"],
        "domingo": ["D", "DOM", "DOMINGO"],
    }

    @classmethod
    def obtener_indices(cls, cabeceras):

        cabeceras = [
            str(c).strip().upper()
            for c in cabeceras
        ]

        resultado = {}

        faltantes = []

        for campo, alias in cls.COLUMNAS.items():

            indice = None

            for nombre in alias:

                if nombre in cabeceras:
                    indice = cabeceras.index(nombre)
                    break

            resultado[campo] = indice

            if indice is None:
                faltantes.append(campo)

        return resultado, faltantes
