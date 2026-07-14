import pandas as pd
from .models import Aula, Programa, Horario, Clase


def importar_datos(ruta_excel):

    # Leer Excel
    df = pd.read_excel(ruta_excel)

    for _, fila in df.iterrows():

        # 1. Crear o buscar aula
        aula, _ = Aula.objects.get_or_create(
            nombre=fila["aula"],
            defaults={"ubicacion": "Importado"}
        )

        # 2. Crear o buscar programa
        programa, _ = Programa.objects.get_or_create(
            nombre=fila["programa"]
        )

        # 3. Crear horario
        horario = Horario.objects.create(
            dia=fila["dia"],
            hora_inicio=fila["hora_inicio"],
            hora_fin=fila["hora_fin"]
        )

        # 4. Crear clase (relación completa)
        Clase.objects.create(
            aula=aula,
            programa=programa,
            horario=horario
        )

    print("✔ Importación completada")