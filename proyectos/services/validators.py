class ExcelValidator:

    """
    Valida que el Excel tenga la información mínima requerida.
    """

    OBLIGATORIOS = {
        "nrc": "identificador de clase",
        "asignatura": "asignatura",
        "docente": "docente",
        "sede": "sede",
        "edificio": "edificio",
        "aula": "espacio o aula",
        "hora_inicio": "hora de inicio",
        "hora_fin": "hora de fin",
    }

    @classmethod
    def validar(cls, indices):

        errores = []

        for campo, etiqueta in cls.OBLIGATORIOS.items():

            if indices.get(campo) is None:

                errores.append(
                    f"Falta la columna requerida: {etiqueta}."
                )

        return errores
