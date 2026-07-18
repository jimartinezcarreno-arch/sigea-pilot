# SIGEA — estado del proyecto y guía técnica

**Fecha:** 18 de julio de 2026
**Producto:** Sistema Inteligente para la Gestión de Espacios Académicos
**Entorno piloto:** [sigea-pilot.onrender.com](https://sigea-pilot.onrender.com/acceso/)

## 1. Resumen ejecutivo

SIGEA ya cuenta con un MVP funcional para que una institución pilotee la consulta de disponibilidad de espacios y la carga de su programación académica desde Excel. El proyecto dejó de ser solo una interfaz: dispone de autenticación, perfiles con permisos, aislamiento por institución, respaldo de importaciones y despliegue público con PostgreSQL.

El avance más valioso es que el flujo central está completo:

1. Un administrador institucional crea cuentas para su institución.
2. Un programador académico importa la programación desde Excel.
3. SIGEA crea o actualiza la estructura de sedes, edificios, aulas y docentes necesaria.
4. Los usuarios consultan disponibilidad, agenda docente, reportes y conflictos de horario.
5. La administración puede consultar el historial y restaurar una programación anterior.

## 2. Funcionalidades logradas

| Área | Estado | Capacidades disponibles |
| --- | --- | --- |
| Acceso institucional | Funcional | Inicio y cierre de sesión, perfiles por institución y validación de pertenencia al tenant. |
| Roles | Funcional | Administrador institucional, Programador académico y Consulta. La interfaz muestra solo las herramientas permitidas. |
| Consulta de espacios | Funcional | Filtros por sede, edificio, aula, docente y hora; tarjetas de espacios libres u ocupados y filtros rápidos. |
| Importación Excel | Funcional | Mapeo flexible de columnas, normalización de datos, creación de estructura faltante, validación y mensajes de resultado. |
| Programación segura | Funcional | Historial de cargas, respaldo previo y restauración por parte del administrador. |
| Agenda docente | Funcional | Vista de lista y calendario semanal con las clases del docente seleccionado. |
| Reportes | Funcional | Ocupación por aula, carga docente, ranking de espacios y tarjetas de métricas. |
| Conflictos | Funcional | Detección de cruces de horario y sugerencia de aula alternativa. |
| Mapa interactivo | Pendiente | Se presenta como “próximamente”; no redirige a una función incompleta. |
| Despliegue | Funcional | Servicio web Django y PostgreSQL administrado en Render, con despliegue desde GitHub. |

## 3. Arquitectura actual

```text
Navegador
  └─ Render / Gunicorn / Django
       ├─ Control de acceso y roles
       ├─ Aislamiento por institución (tenant)
       ├─ Servicios de importación y validación Excel
       ├─ Disponibilidad, agenda, reportes y conflictos
       └─ PostgreSQL de Render
```

### Tecnologías

- **Backend:** Python 3.12 y Django 6.
- **Base de datos:** PostgreSQL en producción; SQLite para desarrollo local.
- **Archivos Excel:** `openpyxl`.
- **Interfaz:** Django Templates, Bootstrap, JavaScript, FullCalendar y Chart.js.
- **Despliegue:** Render, Gunicorn y WhiteNoise para estáticos.
- **Control de versiones:** GitHub, repositorio `jimartinezcarreno-arch/sigea-pilot`.

## 4. Roles y permisos del piloto

| Rol | Puede consultar | Puede importar Excel / reasignar | Puede administrar usuarios e historial |
| --- | --- | --- | --- |
| Consulta | Sí | No | No |
| Programador académico | Sí | Sí | No |
| Administrador institucional | Sí | Sí | Sí |

La cuenta que se entrega a un administrativo de una institución para cargar su archivo debe tener el rol **Programador académico**. La cuenta administradora no debe compartirse durante una prueba.

## 5. Flujo de importación de programación

1. El programador inicia sesión y abre **Consultar aulas**.
2. Descarga la plantilla si necesita una referencia de columnas.
3. Carga el Excel desde el bloque **Importar programación**.
4. El importador identifica columnas equivalentes, valida horas y días, y omite filas sin programación utilizable.
5. Crea sedes, edificios, aulas y docentes faltantes dentro de la institución activa.
6. Guarda un respaldo de las clases previas, reemplaza la programación válida y registra la importación.
7. El administrador puede restaurar una versión previa desde el historial.

### Datos mínimos esperados por fila

- Periodo, NRC, asignatura y docente.
- Sede, edificio y salón/aula.
- Hora de inicio y hora final, en formato `HHMM` o compatible.
- Al menos un día de clase: `L`, `M`, `I`, `J`, `V`, `S` o `D`.

## 6. Revisión de rendimiento realizada hoy

### Hallazgos

1. El plan gratuito de Render puede suspender el servicio cuando no tiene tráfico. Durante la revisión externa, el sitio no respondió dentro de 60 segundos, comportamiento compatible con un *cold start*. Esta demora ocurre antes de que Django procese la página.
2. La pantalla de disponibilidad ejecutaba consultas de clases repetidas para cada aula mostrada. Con una programación institucional grande, el tiempo de respuesta aumentaba proporcionalmente al número de aulas.
3. El dashboard de reportes consultaba la base de datos repetidamente por cada aula y por cada docente.
4. La interfaz carga Bootstrap, íconos, fuentes y algunas librerías desde CDN. Una red institucional lenta puede hacer que el contenido visual tarde más, aunque el servidor ya haya respondido.

### Mejoras aplicadas en esta revisión

- La disponibilidad carga aulas y programación de forma agrupada, evitando consultas repetidas por tarjeta.
- Los reportes calculan sus agregados desde una sola carga de clases, en lugar de consultar por cada aula y docente.
- Se agregaron índices de base de datos para las búsquedas de clases por institución, aula, día, horario y docente.
- El cálculo de “ocupada” considera el día actual, no una clase programada en otro día de la semana.
- Los registros diagnósticos intensivos se redujeron a nivel de depuración para no añadir trabajo y ruido a cada consulta.
- El panel de módulos conserva la visibilidad de herramientas según el rol del usuario.

### Qué esperar después del despliegue

- Tras el primer acceso del día, la navegación interna debería ser notablemente más ágil, especialmente en **Consultar aulas** y **Reportes**.
- Si el primer acceso continúa tardando 30–90 segundos y luego se normaliza, la causa principal será el arranque en frío del plan gratuito de Render.
- Un servicio de pago siempre activo, o una plataforma con instancia persistente, elimina ese tipo de espera de inicio; es una decisión de infraestructura, no de código.

## 7. Validación técnica realizada

Se verificó el cambio con un entorno temporal y aislado de la instalación local:

```text
python manage.py check                         → sin incidencias
python manage.py makemigrations --check        → sin cambios pendientes
python manage.py test proyectos                → 12 pruebas correctas
```

También se comprobó la sintaxis de las vistas, modelos y migración nueva. El entorno virtual local existente apunta a una ruta antigua de Python; no se modificó. Conviene recrearlo antes de la próxima sesión de desarrollo local.

## 8. Limitaciones y riesgos conocidos

- El mapa interactivo, horarios de oficina, cafetería y otros espacios son módulos anunciados, no funcionalidades terminadas.
- El plan gratuito de Render no es apropiado para una demostración que requiera respuesta inmediata constante.
- Los recursos estáticos externos dependen de la conectividad de la institución; a futuro conviene empaquetar o autoalojar los esenciales.
- El reporte de conflictos aún puede requerir una optimización adicional si se importan miles de clases, porque revisa conflictos individualmente.
- La calidad de los resultados depende de que el Excel tenga horarios y días válidos; SIGEA informa y omite las filas que no pueden convertirse en clase.

## 9. Siguiente hoja de ruta recomendada

### Prioridad 1 — Cerrar el piloto

1. Confirmar que el despliegue de Render quede en estado **Live**.
2. Probar con un Excel institucional real desde una cuenta de Programador académico.
3. Validar docentes, aulas, agenda y reportes de la institución piloto.
4. Registrar incidencias y observaciones de los usuarios de prueba.

### Prioridad 2 — Estabilidad SaaS

1. Elegir una instancia de producción sin suspensión para las demostraciones.
2. Configurar copias de seguridad regulares de PostgreSQL.
3. Añadir monitoreo de disponibilidad, tiempos de respuesta y errores.
4. Migrar recursos externos críticos a archivos estáticos propios.

### Prioridad 3 — Evolución funcional

1. Catálogo de tipos de espacios: oficinas, bibliotecas, cafeterías, canchas y parqueaderos.
2. Gestión de reservas y horarios de oficina.
3. Mapa interactivo por sede y edificio.
4. Exportación de reportes e integraciones con sistemas institucionales.

## 10. Operación rápida para una institución piloto

1. Comparte el enlace de acceso: <https://sigea-pilot.onrender.com/acceso/>.
2. Crea una cuenta individual de **Programador académico** para quien realizará la prueba.
3. Pide que conserve el Excel original y documente las columnas utilizadas.
4. Tras importar, revisa:
   - Cantidad de clases informada por SIGEA.
   - Docentes en el filtro y en la agenda.
   - Aulas ocupadas a horas y días de clase.
   - Reportes y posibles conflictos.
5. Si una carga no es correcta, no es necesario borrar datos manualmente: un administrador puede restaurar la programación anterior desde el historial.

---

Este documento describe el estado funcional revisado el 18 de julio de 2026 y sirve como base para las pruebas institucionales y la transición progresiva de SIGEA hacia SaaS.
