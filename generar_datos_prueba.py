import pandas as pd

# Columns list matching the SIGEA Excel importer format
columns = [
    'NOMBRE_DOCENTE', 'IDENTIFICACION_DOCENTE', 'EMAIL_DOCENTE',
    'DESC_SEDE', 'EDIFICIO', 'SALON', 'TIPO_SALON', 'CAPACIDAD_SALON',
    'FACULTAD_RESPONSABLE', 'HI', 'HF',
    'L', 'M', 'I', 'J', 'V', 'S', 'D',
    'METODO_EDUCATIVO'
]

# 1. GENERATE SUCCESSFUL DATA (No conflicts)
data_exito = [
    # Class 1: Fabián on Lunes 08:00-10:00 in AULA 101
    ['PINEDA TORRES FABIAN GIOVANNY', '10987654', 'fabian.pineda@institucion.edu.co',
     'SEDE CENTRAL COLEGIO', 'EDIFICIO A', 'AULA 101', 'AULA', 40,
     'INGENIERIA DE SISTEMAS', '08:00', '10:00',
     'X', '', '', '', '', '', '',
     'RTC'],
     
    # Class 2: Fabián on Martes 10:00-12:00 in AULA 102
    ['PINEDA TORRES FABIAN GIOVANNY', '10987654', 'fabian.pineda@institucion.edu.co',
     'SEDE CENTRAL COLEGIO', 'EDIFICIO A', 'AULA 102', 'AULA', 40,
     'INGENIERIA DE SISTEMAS', '10:00', '12:00',
     '', 'X', '', '', '', '', '',
     'RTC'],
     
    # Class 3: María on Lunes 10:00-12:00 in LAB-301
    ['GARCIA MARIA ANGELICA', '25874139', 'maria.garcia@institucion.edu.co',
     'SEDE CENTRAL COLEGIO', 'EDIFICIO A', 'LAB-301', 'LABORATORIO', 35,
     'BIOTECNOLOGIA', '10:00', '12:00',
     'X', '', '', '', '', '', '',
     'RT1'],
     
    # Class 4: Carlos on Lunes 10:00-12:00 in LAB-301 (RT2 - no overlap because of moments!)
    ['PEREZ CARLOS ALBERTO', '98765432', 'carlos.perez@institucion.edu.co',
     'SEDE CENTRAL COLEGIO', 'EDIFICIO A', 'LAB-301', 'LABORATORIO', 35,
     'BIOTECNOLOGIA', '10:00', '12:00',
     'X', '', '', '', '', '', '',
     'RT2']
]

df_exito = pd.DataFrame(data_exito, columns=columns)
df_exito.to_excel('programacion_exitosa.xlsx', index=False)
print("Creado: programacion_exitosa.xlsx")


# 2. GENERATE CONFLICTING DATA
data_conflictos = [
    # Class 1: Fabián on Lunes 08:00-10:00 in AULA 101
    ['PINEDA TORRES FABIAN GIOVANNY', '10987654', 'fabian.pineda@institucion.edu.co',
     'SEDE CENTRAL COLEGIO', 'EDIFICIO A', 'AULA 101', 'AULA', 40,
     'INGENIERIA DE SISTEMAS', '08:00', '10:00',
     'X', '', '', '', '', '', '',
     'RTC'],
     
    # CONFLICT 1: Classroom Overlap (AULA 101 occupied by another teacher at same time Lunes 08:00-10:00)
    ['GARCIA MARIA ANGELICA', '25874139', 'maria.garcia@institucion.edu.co',
     'SEDE CENTRAL COLEGIO', 'EDIFICIO A', 'AULA 101', 'AULA', 40,
     'BIOTECNOLOGIA', '08:00', '10:00',
     'X', '', '', '', '', '', '',
     'RTC'],
     
    # Class 3: Fabián on Martes 10:00-12:00 in AULA 102
    ['PINEDA TORRES FABIAN GIOVANNY', '10987654', 'fabian.pineda@institucion.edu.co',
     'SEDE CENTRAL COLEGIO', 'EDIFICIO A', 'AULA 102', 'AULA', 40,
     'INGENIERIA DE SISTEMAS', '10:00', '12:00',
     '', 'X', '', '', '', '', '',
     'RTC'],
     
    # CONFLICT 2: Teacher Overlap (Fabián teaching in LAB-301 at same time Martes 10:00-12:00)
    ['PINEDA TORRES FABIAN GIOVANNY', '10987654', 'fabian.pineda@institucion.edu.co',
     'SEDE CENTRAL COLEGIO', 'EDIFICIO A', 'LAB-301', 'LABORATORIO', 35,
     'INGENIERIA DE SISTEMAS', '10:00', '12:00',
     '', 'X', '', '', '', '', '',
     'RTC']
]

df_conflictos = pd.DataFrame(data_conflictos, columns=columns)
df_conflictos.to_excel('programacion_con_conflictos.xlsx', index=False)
print("Creado: programacion_con_conflictos.xlsx")
