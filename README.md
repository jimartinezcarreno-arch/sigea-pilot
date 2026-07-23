# SIGEA - Sistema Inteligente de Gestión de Espacios Académicos

## Descripción del Proyecto

SIGEA es una plataforma web para la gestión eficiente de espacios académicos (aulas, laboratorios, auditorios) en instituciones educativas. Permite consultar disponibilidad en tiempo real, gestionar programación académica, optimizar el uso de infraestructura y detectar conflictos de horarios.

## Características Implementadas

### Dashboard Principal
- **Consulta de disponibilidad de aulas** en tiempo real
- **Filtros rápidos** para espacios libres/ocupados
- **Filtrado por sede, edificio, aula, docente y hora**
- **Visualización de estado** con tarjetas informativas
- **Indicadores de tiempo libre** hasta próxima clase
- **Layout responsivo** con 4-5 tarjetas por fila
- **Agrupación dinámica** de tarjetas filtradas sin espacios vacíos

### Sistema de Autenticación
- **Login seguro** con diseño moderno
- **Gestión de usuarios** con roles
- **Protección de rutas** mediante middleware
- **Soporte multi-tenant** por institución
- **Cierre de sesión** seguro

### Gestión de Programación
- **Importación de Excel** con validación de datos
- **Soporte para múltiples formatos** de columnas
- **Mapeo automático** de sedes, edificios y aulas
- **Creación dinámica** de estructura organizacional
- **Respaldo automático** de programación anterior
- **Historial de importaciones**

### Agenda Docente
- **Vista de calendario** interactiva
- **Filtrado por docente** con buscador
- **Visualización de horarios** por día
- **Detalles de asignaturas** y aulas
- **Integración con FullCalendar**

### Reportes y Análisis
- **Dashboard de métricas** con gráficos
- **Análisis de ocupación** de espacios
- **Estadísticas por docente** y sede
- **Reporte de conflictos** de horarios
- **Reasignación automática** de aulas

### Gestión de Conflictos
- **Detección automática** de superposición de horarios
- **Sugerencias de aulas alternativas**
- **Reasignación con un clic**
- **Validación de disponibilidad**

## Arquitectura Técnica

### Stack Tecnológico
- **Backend:** Django 6.0.4 (Python)
- **Frontend:** HTML5, Bootstrap 5.3.7, JavaScript
- **Base de Datos:** SQLite (desarrollo), PostgreSQL (producción)
- **Deploy:** Render.com
- **Librerías Principales:**
  - openpyxl (manejo de Excel)
  - FullCalendar (calendario interactivo)
  - Chart.js (gráficos)
  - Bootstrap Icons (iconos)

### Estructura del Proyecto
```
planimetria/
├── planimetria/          # Configuración principal de Django
│   ├── settings.py      # Configuración del proyecto
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Configuración WSGI
├── proyectos/           # Aplicación principal
│   ├── models.py        # Modelos de datos
│   ├── views.py         # Vistas y lógica de negocio
│   ├── urls.py          # URLs de la aplicación
│   ├── templates/       # Plantillas HTML
│   ├── services/        # Lógica de servicios
│   │   ├── excel_importer.py  # Importación de Excel
│   │   ├── mappers.py         # Mapeo de columnas
│   │   ├── validators.py      # Validación de datos
│   │   └── asignador_aulas.py # Asignación inteligente
│   ├── middleware.py   # Middleware de autenticación
│   └── management/      # Comandos de gestión
├── static/              # Archivos estáticos
│   ├── css/            # Estilos personalizados
│   └── js/             # JavaScript
├── media/              # Archivos multimedia
└── requirements.txt    # Dependencias de Python
```

### Modelos de Datos Principales

**Institución**
- Multi-tenancy por subdominio
- Configuración de horarios de jornada
- Gestión de sedes y edificios

**Sede, Edificio, Aula**
- Estructura jerárquica de espacios
- Metadatos de capacidad y tipo
- Recursos disponibles

**Docente**
- Información personal y contacto
- Asociación con clases

**Clase**
- Programación académica
- Horarios y asignación de aulas
- Periodo académico

**ImportaciónProgramación**
- Historial de importaciones
- Respaldos de programación

## Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes de Python)
- Git (para control de versiones)

### Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/jimartinezcarreno-arch/sigea-pilot.git
cd sigea-pilot

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor local
python manage.py runserver
```

### Configuración de Variables de Entorno

```bash
# Configuración de producción
DEBUG=False
DJANGO_SECRET_KEY=tu_clave_secreta
ALLOWED_HOSTS=tu_dominio.com
DATABASE_URL=postgresql://usuario:password@host/db
REQUIRE_LOGIN=True
DEFAULT_TENANT_SUBDOMAIN=sigea
PILOT_INSTITUTION_NAME=SIGEA Pilot
```

### Deploy en Render

1. **Conectar repositorio** en dashboard de Render
2. **Configurar servicio web** con `render.yaml`
3. **Configurar base de datos** PostgreSQL
4. **Establecer variables de entorno**
5. **Deploy automático** al hacer push

## Uso del Sistema

### Consulta de Disponibilidad

1. **Acceder al dashboard** principal
2. **Seleccionar filtros** (sede, edificio, aula, docente, hora)
3. **Visualizar estado** de cada aula (libre/ocupada)
4. **Usar filtros rápidos** para ver solo espacios libres u ocupados
5. **Ver detalles** de horarios y tiempo libre

### Importación de Programación

1. **Preparar archivo Excel** con columnas requeridas:
   - NRC, Asignatura, Docente
   - Sede, Edificio, Aula,
   - Hora Inicio, Hora Fin
   - Días de la semana (L-V)

2. **Subir archivo** desde el dashboard
3. **Revisar mensajes** de validación
4. **Verificar resultados** de importación

### Gestión de Conflictos

1. **Acceder a reporte de conflictos**
2. **Ver superposiciones** detectadas
3. **Seleccionar aula alternativa** sugerida
4. **Confirmar reasignación**

### Agenda Docente

1. **Buscar docente** por nombre
2. **Ver calendario** con sus clases
3. **Filtrar por periodo** si es necesario
4. **Consultar detalles** de cada clase

## Funcionalidades Específicas Implementadas

### Filtros Rápidos de Espacios
- **Tarjetas de filtro** en dashboard superior
- **Click para filtrar** espacios libres/ocupados
- **Agrupación automática** sin espacios vacíos
- **Click en "Mostrar todos"** para resetear filtros

### Sistema Multi-Tenant
- **Detección por subdominio** (ej: colegio.sigea.com)
- **Aislamiento de datos** por institución
- **Configuración independiente** por tenant
- **Middleware de acceso** personalizado

### Importación Robusta de Excel
- **Mapeo flexible** de columnas (sinónimos)
- **Validación de formato** de horas
- **Creación automática** de estructura faltante
- **Logging detallado** para depuración
- **Manejo de errores** con mensajes claros

### Diseño Responsivo
- **Adaptación móvil** de dashboard
- **Tarjetas informativas** con información clave
- **Colores semánticos** (verde=libre, rojo=ocupado)
- **Tipografía moderna** con Inter font
- **Animaciones suaves** de transiciones

### Seguridad
- **Autenticación requerida** en producción
- **Protección CSRF** en formularios
- **Validación de entrada** de datos
- **Sanitización de archivos** subidos
- **HTTPS obligatorio** en producción

## Tecnologías y Librerías

### Backend
- **Django 6.0.4** - Framework web
- **openpyxl** - Manejo de Excel
- **dj-database-url** - Configuración de base de datos
- **whitenoise** - Servir archivos estáticos
- **gunicorn** - Servidor WSGI

### Frontend
- **Bootstrap 5.3.7** - Framework CSS
- **Bootstrap Icons 1.11.3** - Iconos
- **FullCalendar 6.1.21** - Calendario interactivo
- **Chart.js** - Gráficos y visualizaciones
- **Inter Font** - Tipografía Google Fonts

### Herramientas de Desarrollo
- **Git** - Control de versiones
- **Render.com** - Plataforma de deploy
- **PostgreSQL** - Base de datos producción

## Estado Actual del Proyecto

### Funcionalidades Completadas ✅
- Dashboard principal con filtros
- Sistema de autenticación completo
- Importación de Excel robusta
- Agenda docente interactiva
- Dashboard de reportes y métricas
- Sistema de detección de conflictos
- Filtros rápidos de espacios
- Diseño responsivo moderno
- Multi-tenancy por institución
- Deploy automatizado en Render

### Limitaciones Conocidas
- **Mapa interactivo** pendiente de implementación
- **Importación de Excel** puede tener problemas con datos preexistentes
- **Sistema de notificaciones** básico (puede mejorarse)

### Próximas Mejoras Sugeridas
- Mapa interactivo con notificaciones
- Sistema de notificaciones avanzado
- Exportación de reportes en PDF/Excel
- API REST para integraciones
- Módulo de reservas de espacios
- Análisis predictivo de ocupación

## Soporte y Mantenimiento

### Logs y Monitoreo
- **Logs de importación** detallados en `excel_importer.py`
- **Logs de autenticación** en middleware
- **Logs de errores** disponibles en Render dashboard

### Respaldo de Datos
- **Respaldo automático** antes de cada importación
- **Historial de importaciones** en base de datos
- **Posibilidad de revertir** cambios

### Actualizaciones
- **Deploy continuo** vía Git push
- **Migraciones automáticas** en cada deploy
- **Colección de archivos estáticos** automatizada

## Contacto y Contribución

**Desarrollado para:** Gestión eficiente de espacios académicos en instituciones educativas

**Versión Actual:** 1.0 (Producción en Render)

**Estado:** Activo para pruebas institucionales con autenticación

---

*Última actualización: Julio 2026*
*Documentación generada automáticamente basada en el estado actual del proyecto*
