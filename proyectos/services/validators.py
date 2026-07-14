class ExcelValidator:

    """
    Valida que el Excel tenga la información mínima requerida.
    """

    OBLIGATORIOS = [

        "nrc",
        "asignatura",
        "docente",
        "sede",
        "edificio",
        "aula",
        "hora_inicio",
        "hora_fin",

    ]

    @classmethod
    def validar(cls, indices):

        errores = []

        for campo in cls.OBLIGATORIOS:

            if indices.get(campo) is None:

                errores.append(
                    f"No se encontró la columna '{campo}'"
                )

        return errores