# SIGEA 2.0 - Requerimientos
## Visión Estratégica

**SIGEA (Core):** Sistema Inteligente de Gestión de Espacios Académicos
- Enfoque: Gestión de aulas, horarios, disponibilidad, optimización de infraestructura
- Mercado: Colegios, universidades, institutos técnicos

**SIGEA School (Complemento):** Sistema Educativo Completo
- Enfoque: Gestión de estudiantes, calificaciones, matrículas, asistencia
- Mercado: Colegios que requieren gestión académica integral

---

## SIGEA 2.0 - Roadmap

### Fase 1: Solidificar Core SIGEA

#### 1.1 Mejorar Gestión de Espacios Existente
**Objetivo:** Optimizar funcionalidades actuales de gestión de espacios

**Funcionalidades:**
- Mejorar filtros de búsqueda de aulas
- Optimizar consultas de disponibilidad
- Mejorar detección de conflictos
- Agregar sugerencias inteligentes de reasignación
- Dashboard de métricas de ocupación

**Prioridad:** Alta
**Impacto:** Mejora UX de usuarios existentes

#### 1.2 Mapa Interactivo (Prioridad Alta)
**Objetivo:** Visualización y navegación de espacios en tiempo real

**Funcionalidades:**
- **Navegación básica:**
  - Búsqueda de espacios por nombre/código
  - Cálculo de ruta óptima (algoritmo Dijkstra/A*)
  - Navegación paso a paso
  - Instrucciones visuales

- **Ocupación en tiempo real:**
  - Estado libre/ocupado en mapa
  - Detalles al hacer clic (docente, asignatura)
  - Integración con datos de horarios
  - Indicadores de tiempo libre

- **Importación de planos:**
  - Carga de planos de edificios
  - Georeferenciación manual
  - Edición visual de espacios
  - Soporte para múltiples pisos

- **Rutas de evacuación:**
  - Rutas predefinidas sobre planos
  - Modo de emergencia
  - Alertas visuales y sonoras
  - Notificaciones push

**Prioridad:** Alta
**Impacto:** Diferenciador competitivo clave

#### 1.3 Offline-First Básico
**Objetivo:** Permitir uso en colegios rurales con poca conectividad

**Funcionalidades:**
- Service Workers para caché de datos
- IndexedDB para almacenamiento local
- Caché de datos frecuentes (aulas, horarios)
- Modo lectura offline
- Sincronización cuando hay conexión
- Indicador de estado de conexión

**Prioridad:** Alta
**Impacto:** Diferenciador para mercado rural

#### 1.4 2FA (Autenticación de Dos Factores)
**Objetivo:** Máxima seguridad para datos sensibles

**Funcionalidades:**
- Google Authenticator (TOTP)
- SMS como alternativa
- Códigos de recuperación
- Configuración por usuario
- Opcional pero recomendado

**Prioridad:** Alta
**Impacto:** Cumplimiento de seguridad

#### 1.5 Auditoría Completa
**Objetivo:** Registro de todas las acciones importantes

**Funcionalidades:**
- Registro de LOGIN/LOGOUT
- Registro de consultas (qué, cuándo, quién)
- Registro de importaciones
- Registro de modificaciones de datos
- IP address y user agent
- Reportes de actividad
- Alertas de comportamiento sospechoso

**Prioridad:** Alta
**Impacto:** Seguridad y compliance

---

### Fase 2: Extensiones Estratégicas (6-8 semanas)

#### 2.1 Asistencia QR Simple
**Objetivo:** Confirmar que el docente está en el aula dando clase

**Funcionalidades:**
- Generación de QR dinámico por aula
- Escaneo por docente al inicio de clase
- Registro de asistencia (entradas/salidas)
- Verificación de horario programado
- Reportes de asistencia
- Alertas de inasistencia
- **Sin:** Geofencing, biometría, ubicación

**Prioridad:** Alta
**Impacto:** Garantiza uso efectivo de espacios

#### 2.2 Tablón de Anuncios
**Objetivo:** Comunicación unidireccional institucional

**Funcionalidades:**
- Publicación de anuncios por institución
- Prioridad (normal, urgente, informativo)
- Audiencia (todos, estudiantes, docentes)
- Historial de anuncios
- Fechas de publicación/expiración
- Notificaciones push

**Prioridad:** Media
**Impacto:** Mejora comunicación

#### 2.3 API REST Básica
**Objetivo:** Integración con otros sistemas institucionales

**Funcionalidades:**
- Endpoints principales:
  - `/api/v1/aulas/`
  - `/api/v1/docentes/`
  - `/api/v1/edificios/`
  - `/api/v1/horarios/`
- Autenticación por token (JWT)
- Rate limiting
- Documentación Swagger/OpenAPI
- Versionado de API

**Prioridad:** Media
**Impacto:** Integraciones futuras

#### 2.4 Reportes Avanzados
**Objetivo:** Exportación y análisis de datos

**Funcionalidades:**
- Exportación a PDF
- Exportación a Excel
- Filtros temporales (por período, momento académico)
- Gráficos interactivos (Chart.js mejorado)
- Reportes de ocupación
- Reportes de conflictos
- Generación programada (opcional)

**Prioridad:** Media
**Impacto:** Análisis de datos

#### 2.5 OAuth Institucional (Google/Microsoft)
**Objetivo:** Permitir login con credenciales institucionales (Gmail/Outlook)

**Funcionalidades:**
- **Google OAuth (G Suite/Workspace):**
  - Login con cuenta Google institucional
  - Verificación de dominio autorizado
  - Creación automática de usuario local
  - Sincronización de perfil

- **Microsoft OAuth (Azure AD/Office 365):**
  - Login con cuenta Microsoft institucional
  - Integración con Azure AD
  - Verificación de tenant institucional
  - Creación automática de usuario local

- **Configuración:**
  - OAuth opcional (no obligatorio)
  - Mantener login tradicional como alternativa
  - Configuración por institución
  - Dominios autorizados por institución

**Prioridad:** Media
**Impacto:** Mejora UX para instituciones con Workspace/Office 365, SSO

---

### Fase 3: Opcionales (Solo si hay demanda)

#### 3.1 Módulo Financiero
**Objetivo:** Gestión de pagos de estudiantes a la institución

**Funcionalidades:**
- Gestión de conceptos de pago (mensualidades, matrículas)
- Registro de pagos manuales
- Generación de facturas (PDF)
- Reportes de recaudo
- Estado de cuenta por estudiante
- Alertas de pagos pendientes
- **Sin:** Integración automática con pasarelas de pago

**Prioridad:** Baja
**Impacto:** Complementario a gestión de espacios

#### 3.2 Integración SIMAT
**Objetivo:** Exportación de datos compatible con Ministerio de Educación

**Funcionalidades:**
- Exportación de datos de estudiantes
- Formato compatible con SIMAT
- Validación de documentos
- Reportes obligatorios
- **Sin:** Sincronización automática bidireccional

**Prioridad:** Baja
**Impacto:** Compliance Colombia

---

## SIGEA School - Complemento Educativo

### Visión
**SIGEA School:** Extensión educativa completa de SIGEA Core

**Relación con SIGEA Core:**
- Comparte infraestructura (multi-tenancy, autenticación, seguridad)
- Comparte gestión de espacios (aulas, horarios)
- Agrega gestión académica (estudiantes, calificaciones, matrículas)
- Opcional: instituciones pueden usar solo SIGEA Core o SIGEA Core + School

### Módulos SIGEA School

#### 1. Gestión de Estudiantes
- Registro de estudiantes
- Datos personales y contacto
- Acudientes/responsables
- Historial académico
- Búsqueda avanzada

#### 2. Matrículas
- Gestión de matrículas por período
- Asignación a grados y grupos
- Estados de matrícula
- Historial de matrículas

#### 3. Calificaciones y Boletines
- Registro de calificaciones por asignatura
- Cálculo automático de promedios
- Generación de boletines (PDF)
- Comparación histórica
- Alertas de bajo rendimiento

#### 4. Asistencia Estudiantil
- Registro de asistencia de estudiantes
- Reportes de inasistencia
- Estadísticas de asistencia
- Integración con asistencia QR docente

#### 5. Comunicación
- Mensajería docente-coordinadores
- Comunicación con acudientes
- Notificaciones push

#### 6. Dashboard Educativo
- Métricas de matrículas
- Análisis de rendimiento académico
- Estadísticas de asistencia
- Reportes financieros básicos

---

## Arquitectura Técnica

### Stack Tecnológico SIGEA 2.0

**Backend:**
- Django 6.0.4
- Django REST Framework (para API)
- PostgreSQL (producción)
- SQLite (offline)
- Celery + Redis (tareas asíncronas)

**Frontend:**
- Django Templates (actual)
- Bootstrap 5.3.7
- PWA (Progressive Web App)
- Service Workers
- IndexedDB

**Seguridad:**
- Django Guardian (permisos granulares)
- django-otp (2FA)
- Rate limiting
- HTTPS obligatorio

**Testing:**
- pytest + pytest-django
- Coverage.py
- Tests unitarios en módulos críticos

---

## Cronograma de Implementación

### SIGEA 2.0 Core
- **Fase 1:** 4-6 semanas
- **Fase 2:** 6-8 semanas
- **Total:** 10-14 semanas (2.5-3.5 meses)

### SIGEA School (Opcional)
- **Fase 1:** 8-10 semanas
- **Fase 2:** 4-6 semanas
- **Total:** 12-16 semanas (3-4 meses)

**Total con SIGEA School:** 22-30 semanas (5.5-7.5 meses)

---

## Estrategia de Monetización

### SIGEA 2.0 Core

**Básico:**
- Gestión de espacios
- Consulta de disponibilidad
- Programación académica
- Detección de conflictos
- $30,000,000 COP/año

**Pro:**
- Todo Básico +
- Mapa interactivo
- Offline-first
- Asistencia QR
- Tablón de anuncios
- $80,000,000 COP/año

**Premium:**
- Todo Pro +
- API REST
- Reportes avanzados
- Auditoría completa
- 2FA
- $150,000,000 COP/año

### SIGEA School (Add-on)

**Add-on Básico:**
- Gestión de estudiantes
- Matrículas
- Calificaciones básicas
- $50,000,000 COP/año adicional

**Add-on Completo:**
- Todo Add-on Básico +
- Boletines
- Asistencia estudiantil
- Comunicación
- Dashboard educativo
- $100,000,000 COP/año adicional

---

## Ventaja Competitiva

### Diferenciadores SIGEA 2.0
1. **Offline-first:** Funciona en colegios rurales
2. **Mapa interactivo:** Navegación y evacuación
3. **Asistencia QR:** Garantiza docente en aula
4. **Diseño moderno:** vs interfaces arcaicas
5. **Multi-tenancia robusta:** Escalable

### Diferenciadores SIGEA School
1. **Integración nativa** con SIGEA Core
2. **Mobile-first:** Funciona perfectamente en móviles
3. **Offline-first:** Para zonas rurales
4. **Integración SIMAT:** Compliance Colombia
5. **Modular:** Solo lo que necesitas

---

## Próximos Pasos Inmediatos

### Esta Semana
1. Revertir modelos educativos agregados (son para SIGEA School)
2. Actualizar README con visión SIGEA 2.0
3. Documentar arquitectura SIGEA Core + School
4. Planificar implementación de Mapa Interactivo

### Próximas 2 Semanas
1. Comenzar implementación de Mapa Interactivo
2. Configurar Service Workers para offline-first
3. Implementar sistema de auditoría básico
4. Configurar 2FA con django-otp

---

## Conclusión

**SIGEA 2.0:** Enfoque en gestión de espacios con extensiones estratégicas que no desvían el objetivo principal.

**SIGEA School:** Complemento educativo opcional para instituciones que requieren gestión académica integral.

**Estrategia:** SIGEA Core como producto principal, SIGEA School como upsell para colegios que requieren más funcionalidades.
