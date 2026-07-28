# SIGEA Core

> Sistema Inteligente para la Gestión de Espacios Académicos.

SIGEA ayuda a una institución a cargar su programación académica, consultar la disponibilidad de sus espacios y resolver conflictos de horario con una única fuente de información. El producto se concentra en **espacios, programación y ocupación**; cualquier módulo ajeno a ese núcleo queda fuera de este repositorio y de esta hoja de ruta.

## Estado, validado el 28 de julio de 2026

**SIGEA es hoy un piloto institucional funcional con base multi-institución.** Está listo para seguir validándose con instituciones reales bajo acompañamiento. Aún no es un SaaS comercial listo para vender de forma autoservicio: faltan capacidades de operación, seguridad, aprovisionamiento y producto que permiten atender muchas instituciones de forma confiable.

La distinción es deliberada:

| Nivel | Estado | Qué significa |
| --- | --- | --- |
| Piloto institucional | En operación | Una institución puede crear cuentas, cargar programación, consultar espacios, revisar conflictos y recuperar una importación anterior. |
| SaaS comercial | En preparación | Falta el flujo autoservicio de alta de institución, observabilidad, soporte operativo, planes, auditoría y controles de seguridad ampliados. |

### Verificaciones realizadas

- `python manage.py check`: sin incidencias.
- `python manage.py test proyectos`: **12 pruebas aprobadas**.
- Despliegue configurado en Render con PostgreSQL, migraciones, archivos estáticos y arranque del piloto.
- Repositorio protegido de secretos, base local, archivos multimedia y Excel mediante `.gitignore`.

Las pruebas actuales cubren aislamiento básico entre instituciones, roles, agenda docente, reasignación de conflictos, restauración de importaciones y carga de Excel. No sustituyen una prueba de aceptación con datos reales ni pruebas de navegador de extremo a extremo.

## Qué funciona hoy

### Núcleo de producto

- Consulta de aulas por sede, edificio, aula, docente y hora.
- Estado libre u ocupado, próxima clase y programación asociada a cada espacio.
- Filtros rápidos y cuadrícula responsiva: una tarjeta en móvil, dos o tres en portátil y cuatro o cinco en pantalla amplia.
- Agenda docente con lista y calendario recurrente.
- Dashboard de reportes y detección de cruces de horario.
- Sugerencia y reasignación manual de un aula alternativa cuando existe disponibilidad.

### Programación e información institucional

- Importación de Excel con mapeo flexible de encabezados.
- Creación controlada de sedes, edificios, aulas y docentes que no existen aún en el catálogo.
- Validación de formatos de hora y omisión de filas inválidas, conservando la programación anterior si no hay clases válidas para importar.
- Plantilla de Excel descargable.
- Historial de importaciones y restauración de una programación previa.

### Acceso y separación por institución

- Roles: administrador institucional, programador académico y consulta.
- Restricción de acciones sensibles por rol: usuarios, importación y reasignación.
- Asociación de cada usuario con una institución.
- Aislamiento lógico de consultas por institución mediante middleware y `ContextVar`.
- Autenticación requerida en el entorno de piloto de Render.

### Plataforma actual

- Django 6, PostgreSQL en producción y SQLite para desarrollo local.
- Render Blueprint con despliegue desde `main`.
- WhiteNoise para estáticos de producción.
- Índices de base de datos para búsquedas frecuentes de clases por aula, docente, día y horario.

## Lo que no debemos presentar como terminado

Estos puntos son importantes porque una documentación honesta evita ofrecer a una institución una capacidad que todavía no existe.

| Área | Estado real | Decisión |
| --- | --- | --- |
| Mapa interactivo | Hay una ruta y un prototipo SVG, pero el código de mapa aún conserva referencias de un modelo anterior de planos. No existe un flujo institucional para subir, calibrar y publicar planos reales. | Mantenerlo fuera de la promesa comercial hasta reconstruirlo como módulo independiente. |
| Alta autoservicio de instituciones | La separación lógica existe, pero la creación de una nueva institución, su dominio, su administrador y su catálogo no es un flujo de producto. | Construir aprovisionamiento de tenants antes de abrir el servicio a varias instituciones. |
| Importación para operación masiva | La carga funciona y conserva respaldo; aún no ofrece vista previa, conciliación de cambios, reporte descargable ni aprobación explícita antes de reemplazar una programación. | Es el siguiente frente funcional prioritario. |
| Catálogo de espacios | Se puede completar desde la importación o el admin de Django, pero no hay gestión institucional completa en la interfaz. | Crear administración de sedes, edificios, aulas, capacidad y recursos. |
| Seguridad SaaS | Hay autenticación, roles, CSRF, HTTPS y cookies seguras en producción. Faltan límites de intentos, restablecimiento de contraseña, 2FA, auditoría de eventos, política de sesiones y revisión de permisos por funcionalidad. | Endurecer antes de una venta o apertura general. |
| Operación | El despliegue y las migraciones están automatizados, pero faltan salud pública, alertas, monitoreo, trazas, política de respaldo y recuperación documentada. | Establecer una línea base operativa antes de depender de SIGEA a diario. |
| Integraciones | No hay API pública versionada, SSO institucional, correo transaccional ni colas de trabajo. | Postergar hasta tener el núcleo validado y repetible. |
| Facturación y planes | No existen suscripciones, límites de uso, facturación ni entitlements. | Diseñar después de validar propuesta de valor y disposición de pago. |

## Arquitectura actual

```text
planimetria/
├── planimetria/                 # Configuración Django, URLs y WSGI/ASGI
├── proyectos/                   # Aplicación principal de SIGEA
│   ├── models.py                # Instituciones, usuarios, espacios, clases e importaciones
│   ├── middleware.py            # Resolución y acceso por institución
│   ├── role_middleware.py       # Restricciones por rol
│   ├── services/                # Importación, validación, respaldo y asignación
│   ├── templates/               # Interfaz web actual
│   ├── management/commands/     # Bootstrap y tareas administrativas
│   └── tests.py                 # Pruebas de núcleo y piloto
├── static/                      # CSS y JavaScript compartidos
├── render.yaml                  # Despliegue del piloto
└── requirements.txt
```

El modelo de datos vigente cubre `Institucion`, `PerfilUsuario`, `Sede`, `Edificio`, `Aula`, `Docente`, `PeriodoAcademico`, `MomentoAcademico`, `Clase` e `ImportacionProgramacion`.

## Arquitectura objetivo para SaaS

No se debe reescribir SIGEA ahora. La evolución recomendada es separar responsabilidades gradualmente, conservando los modelos y las funcionalidades que ya funcionan.

```text
config/
├── settings/
│   ├── base.py                  # Ajustes compartidos
│   ├── development.py            # Desarrollo local
│   ├── test.py                   # Pruebas
│   └── production.py             # Seguridad y operación de producción
apps/
├── tenants/                     # Instituciones, dominios, membresías y aprovisionamiento
├── identities/                  # Roles, sesiones, recuperación y SSO futuro
├── spaces/                      # Sedes, edificios, aulas, recursos y catálogo
├── scheduling/                  # Periodos, clases, disponibilidad y conflictos
├── imports/                     # Plantillas, previsualización, validación e historial
├── analytics/                   # Métricas y exportaciones
├── audit/                       # Eventos y trazabilidad
└── maps/                        # Planos y navegación, solo cuando el núcleo esté estable
api/
└── v1/                          # Contratos versionados para integraciones futuras
tests/
├── unit/
├── integration/
└── e2e/
```

Esta estructura es una meta de organización, no una tarea de migración masiva. Cada módulo debe extraerse únicamente cuando el siguiente incremento lo requiera.

## Hoja de ruta hacia SaaS

### Fase 0 — Consolidar el piloto

**Objetivo:** que una institución pueda operar un periodo académico completo sin depender de intervención técnica.

1. Corregir los detalles de experiencia detectados en las pruebas reales: codificación de textos, responsive, mensajes de error y rutas incompletas.
2. Terminar la importación segura:
   - previsualización antes de aplicar;
   - total de filas válidas, inválidas y cambios esperados;
   - reporte descargable de errores;
   - confirmación explícita para reemplazar la programación;
   - conciliación de aulas y docentes creados automáticamente.
3. Convertir el catálogo de espacios en una pantalla institucional: capacidad, tipo, recursos, sede y edificio.
4. Definir una prueba de aceptación con la institución piloto y ejecutar una importación de un periodo real en un entorno de prueba.
5. Mantener el mapa fuera de navegación activa hasta que los modelos, el almacenamiento de planos y la interfaz estén alineados.

**Criterio de salida:** una persona administrativa completa una carga, interpreta el resultado, consulta disponibilidad y revierte una carga sin ayuda técnica.

### Fase 1 — Base operativa SaaS

**Objetivo:** soportar varias instituciones sin mezclar datos ni depender de operaciones manuales peligrosas.

1. Separar ajustes de Django para desarrollo, pruebas y producción.
2. Crear aprovisionamiento de institución: nombre, subdominio o dominio, administrador inicial, jornada, plan y estado.
3. Formalizar membresías y permisos por funcionalidad; evitar que la seguridad dependa solo de rutas.
4. Añadir auditoría inmutable de accesos, importaciones, restauraciones, altas de usuarios y reasignaciones.
5. Agregar endpoint de salud, registro estructurado, alertas de error, monitoreo de disponibilidad y política de respaldo/restauración.
6. Mover archivos institucionales y futuros planos a almacenamiento de objetos; los archivos locales no son una base SaaS confiable.
7. Incluir límites de carga, control de tasa de inicio de sesión y recuperación de contraseña por correo.

**Criterio de salida:** se pueden crear dos instituciones, cada una con sus usuarios y datos aislados, monitorear el servicio y recuperar información documentadamente.

### Fase 2 — Producto repetible

**Objetivo:** que SIGEA se pueda instalar y entender sin acompañamiento constante del equipo técnico.

1. Asistente de bienvenida con carga inicial de catálogo y plantilla de programación.
2. Centro de importaciones con estado, validación, historial y restauración.
3. Reportes de ocupación y conflictos que respondan preguntas operativas concretas.
4. Exportación de reportes y criterios de negocio por capacidad, tipo de aula y recursos requeridos.
5. Pruebas de navegador para los flujos críticos: inicio de sesión, importación, filtros, conflictos, roles y restauración.
6. Manual breve para administrador institucional y canal de soporte para el piloto.

**Criterio de salida:** una segunda institución puede configurarse, capacitarse y completar el flujo principal con documentación.

### Fase 3 — Comercialización controlada

**Objetivo:** convertir el piloto repetible en un servicio comercial.

1. Definir planes según número de espacios, usuarios, sedes o volumen de importaciones.
2. Implementar entitlements antes de integrar cobro: qué puede usar cada plan y cuáles son sus límites.
3. Preparar facturación, términos del servicio, tratamiento de datos, acuerdos de soporte y proceso de baja/exportación de datos.
4. Agregar dominios personalizados y SSO institucional solo cuando existan clientes que lo requieran.
5. Establecer métricas de disponibilidad, tiempos de respuesta, respaldo y soporte acordes al plan contratado.

**Criterio de salida:** cada institución conoce su plan, límites, responsable de datos, canal de soporte y proceso de contratación.

### Fase 4 — Diferenciadores, después de validar el núcleo

- Mapa de planos institucionales con carga, calibración y publicación por edificio.
- Reservas de auditorios, laboratorios u otros recursos compartidos.
- API versionada para integraciones académicas.
- SSO, 2FA y automatizaciones avanzadas.
- Analítica predictiva solo cuando exista suficiente historial confiable.

## Por dónde empezar ahora

La prioridad recomendada para el próximo incremento es **la previsualización y conciliación de importación Excel**.

Es la puerta de entrada de los datos que alimentan disponibilidad, agenda, conflictos y reportes. Si ese flujo es confiable, una institución puede probar SIGEA de verdad; si falla, ninguna mejora visual o de mapa compensará la desconfianza en la información.

Orden de trabajo sugerido:

1. Recopilar el Excel real de la institución piloto y acordar una plantilla canónica.
2. Diseñar una pantalla de previsualización: filas válidas, errores, aulas nuevas, docentes nuevos y resumen de cambios.
3. Aplicar cambios solo tras confirmación del programador académico.
4. Generar un reporte de resultado descargable y conservar el respaldo actual.
5. Ejecutar una prueba de aceptación con el administrativo de la institución.
6. Después, construir la administración de catálogo de espacios.

## Métricas para decidir si SIGEA avanza

Durante el piloto se deben medir hechos, no solo impresiones:

- Tiempo de una importación hasta una programación utilizable.
- Porcentaje de filas válidas en la primera carga y causas frecuentes de error.
- Exactitud percibida de la disponibilidad frente a la programación oficial.
- Número de conflictos encontrados y resueltos.
- Tiempo que toma encontrar un espacio disponible.
- Usuarios activos por rol y frecuencia de uso semanal.
- Incidencias de soporte, tiempo de respuesta y restauraciones necesarias.
- Instituciones que completarían una segunda carga sin acompañamiento.

Si estas métricas mejoran y al menos dos instituciones recorren el flujo completo con datos aislados, SIGEA tendrá evidencia real para pasar de piloto a producto SaaS.

## Operación local

```bash
python -m venv venv
# Windows
venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py bootstrap_pilot
python manage.py runserver
```

Antes de enviar cambios:

```bash
python manage.py check
python manage.py test proyectos
```

Las variables locales de referencia están en [`.env.example`](.env.example). Las credenciales y valores de producción deben configurarse exclusivamente como variables seguras del proveedor de despliegue.

## Principios de desarrollo

1. Una institución nunca debe leer ni modificar datos de otra.
2. Ninguna importación debe destruir información sin respaldo, revisión y trazabilidad.
3. Cada funcionalidad nueva debe resolver un problema medible de gestión de espacios.
4. La simplicidad operativa vale más que una función llamativa sin adopción.
5. Todo flujo crítico necesita pruebas automatizadas y una prueba manual de aceptación.

---

- **Producto:** SIGEA Core
- **Estado:** piloto institucional en consolidación
- **Última validación documental:** 28 de julio de 2026
