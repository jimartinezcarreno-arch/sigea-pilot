class ExcelMapper:

    """
    Traduce las columnas del Excel al modelo interno de SIGEA.
    """

    COLUMNAS = {

        "periodo": [
            "PERIODO",
        ],

        "nrc": [
            "NRC",
        ],

        "asignatura": [
            "TITULO",
            "ASIGNATURA",
            "MATERIA",
            "CURSO",
        ],

        "docente": [
            "NOMBRE_DOCENTE",
            "DOCENTE",
            "PROFESOR",
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
        ],

        "hora_inicio": [
            "HI",
            "HORA INICIO",
            "HORA_INICIO",
        ],

        "hora_fin": [
            "HF",
            "HORA FIN",
            "HORA_FINAL",
        ],

        "lunes": ["L"],
        "martes": ["M"],
        "miercoles": ["I"],
        "jueves": ["J"],
        "viernes": ["V"],
        "sabado": ["S"],
        "domingo": ["D"],
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