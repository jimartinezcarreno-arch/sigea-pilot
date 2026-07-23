# SIGEA - Documentación de Peticiones para Validación

## Estado Actual del Sistema (Julio 2026)

### Funcionalidades Implementadas

**1. Sistema de Consulta de Aulas**
- Consulta en tiempo real de disponibilidad de aulas
- Filtrado por sede, edificio, aula y docente
- Visualización de estado (libre/ocupada) según hora de consulta
- Cálculo de tiempo libre hasta próxima clase
- Dashboard de reportes y detección de conflictos

**2. Importación de Programación Excel**
- Carga masiva de horarios académicos desde Excel
- Creación automática de sedes, edificios, aulas y docentes
- Validación de datos y manejo de errores
- Historial de importaciones con capacidad de restauración
- **Corrección reciente:** Estrategia mejorada para omitir filas con errores en lugar de cancelar toda la importación

**3. Dashboard de Módulos (Nuevo)**
- Página de selección de módulos después del login
- 4 opciones disponibles:
  - Consultar Aulas (funcional)
  - Horarios de Oficina (próximamente)
  - Cafetería (próximamente)
  - Otros Espacios (próximamente)
- Diseño responsive optimizado para móviles, tablets y desktop
- Interfaz moderna con gradientes y animaciones

**4. Gestión de Usuarios**
- Creación de cuentas individuales por institución
- Roles: Administrador, Programador Académico, Consulta
- Sistema multi-tenant con aislamiento de datos

### Correcciones Recientes

**1. Importación Excel (Julio 2026)**
- **Problema:** Filas con rangos de horas inválidos cancelaban toda la importación
- **Solución:** Cambio de estrategia para omitir filas con errores y continuar con las válidas
- **Resultado:** Mejor tolerancia a errores en datos de entrada

**2. Dashboard de Módulos (Julio 2026)**
- **Problema:** Error 500 del servidor por template base.html inexistente
- **Solución:** Conversión a HTML completo sin herencia de templates
- **Resultado:** Dashboard funcional como página de inicio post-login

**3. Responsive Dashboard (Julio 2026)**
- **Problema:** Diseño no optimizado para diferentes tamaños de pantalla
- **Solución:** Implementación de media queries para móviles, tablets y desktop
- **Resultado:** Experiencia consistente en todos los dispositivos

---

## Visión del Producto

**SIGEA (Sistema Inteligente de Gestión de Espacios Académicos)** es una plataforma SaaS para la gestión integral de espacios físicos en instituciones educativas, con enfoque en:

- **Navegación innovadora** dentro del campus
- **Accesibilidad universal** para personas con discapacidad visual
- **Optimización de espacios** para administración
- **Experiencia usuario** superior a soluciones tradicionales

---

## Peticiones Principales del Cliente

### 1. Navegación Innovadora al Destino

**Requerimiento:** Sistema que lleve al usuario a su destino dentro de la institución de manera innovadora.

**Estado Actual:** El cliente referencia ArcGIS IPS (Indoor Positioning System) de ETH Zurich como ejemplo deseado.

**Restricción:** Si la solución es costosa, no se implementará de esa forma.

**Alternativas a Validar:**
- Wi-Fi Fingerprinting (costo $0, usa infraestructura existente)
- QR Codes + GPS Híbrido (costo $50-100, precisión en puntos clave)
- Ultrasonic Positioning (costo $10-20/beacon, mayor precisión)
- Bluetooth Beacons (costo $20-50/beacon, solución ArcGIS IPS)

**Preguntas de Validación:**
- ¿Qué nivel de precisión es aceptable? (1-3 metros vs 3-5 metros)
- ¿Es crítico el tracking en tiempo real o basta navegación punto a punto?
- ¿Qué presupuesto está disponible para hardware?
- ¿Prefieren solución 100% software o están dispuestos a invertir en hardware?

### 2. Gestión de Todos los Espacios Físicos

**Requerimiento:** No solo aulas académicas, sino todos los espacios de la institución.

**Estado Actual:**
- **Académicos:** Aulas, laboratorios, auditorios (implementados)
- **Administrativos:** Oficinas, horarios de atención (dashboard creado, funcionalidad pendiente)
- **Servicios:** Cafeterías, bibliotecas, canchas deportivas (dashboard creado, funcionalidad pendiente)
- **Complementarios:** Parqueaderos, zonas verdes, enfermería (pendiente)

**Tipos de Espacios Solicitados:**
- **Académicos:** Aulas, laboratorios, auditorios (ya implementados)
- **Administrativos:** Oficinas, horarios de atención (nuevo)
- **Servicios:** Cafeterías, bibliotecas, canchas deportivas (nuevo)
- **Complementarios:** Parqueaderos, zonas verdes, enfermería (nuevo)

**Funcionalidades por Tipo:**
- **Oficinas:** Horarios de atención, sistema de citas
- **Cafeterías:** Horarios de servicio, capacidad de aforo
- **Canchas:** Reservas, horarios de uso
- **Bibliotecas:** Zonas de estudio, disponibilidad de cubículos

**Preguntas de Validación:**
- ¿Qué tipo de espacios es prioritario implementar primero?
- ¿Necesitan sistema de reservas para canchas/auditorios?
- ¿El sistema de citas para oficinas es crítico o puede ser fase posterior?
- ¿Qué metadatos adicionales necesitan por tipo de espacio?

### 3. Accesibilidad por Voz

**Requerimiento:** Formato de voz para personas con discapacidad visual.

**Estado Actual:** Propuesta de Web Speech API + Screen Reader Integration.

**Funcionalidades Propuestas:**
- Comandos de voz: "Llévame a la cafetería"
- Exploración auditiva del mapa
- Feedback sonoro de navegación
- Alto contraste WCAG AA/AAA
- Compatibilidad con NVDA, JAWS, VoiceOver

**Preguntas de Validación:**
- ¿Es prioritario el asistente conversacional o basta comandos básicos?
- ¿Necesitan multi-idioma o solo español?
- ¿Qué nivel de detalle en las descripciones auditivas?
- ¿Tienen usuarios ciegos para beta testing?

### 4. Roles de Usuario

**Requerimiento:** Diferentes funcionalidades según rol.

**Roles Identificados:**
- **Estudiantes:** Consulta pública sin autenticación, mapa interactivo, horarios
- **Docentes:** Agenda docente, horarios de oficina, mapa
- **Administrativos:** Gestión completa de espacios, reportes, optimización

**Preguntas de Validación:**
- ¿Necesitan rol adicional para personal de servicios?
- ¿Los estudiantes requieren autenticación para alguna funcionalidad?
- ¿Qué permisos específicos por rol administrativo?
- ¿Necesitan jerarquía dentro de administrativos?

---

## Alternativas Tecnológicas a Validar

### Opción A: Wi-Fi Fingerprinting (Recomendada para MVP)

**Descripción:** Usa señales Wi-Fi existentes para triangulación de posición.

**Ventajas:**
- Costo: $0 (software puro)
- Usa infraestructura Wi-Fi existente
- Precisión: 3-5 metros (aceptable para navegación)
- Sin hardware adicional
- Mantenimiento mínimo

**Desventajas:**
- Menor precisión que beacons
- Requiere calibración inicial
- Dependencia de cobertura Wi-Fi

**Herramientas:** Cisco CMX, Aruba Meridian, OpenSource

**Viabilidad:** ✅ Alta - Ideal para MVP y validación

---

### Opción B: QR Codes + GPS Híbrido

**Descripción:** QR codes en puntos clave + GPS outdoor.

**Ventajas:**
- Costo: $50-100 (impresión de QR codes)
- Precisión: 1-2 metros (en puntos QR)
- Sin dependencia de hardware complejo
- Fácil implementación

**Desventajas:**
- Requiere acción del usuario (escanear QR)
- No tracking continuo
- Dependencia de GPS outdoor

**Viabilidad:** ✅ Media - Buena para complementar otras soluciones

---

### Opción C: Bluetooth Beacons (ArcGIS IPS) - Opción Recomendada para Educación

**Descripción:** Beacons Bluetooth LE para posicionamiento indoor con ArcGIS IPS.

**Ventajas:**
- Precisión: 1-3 metros (sub-métrica)
- Tracking continuo en tiempo real
- Experiencia usuario similar a Google Maps indoor
- Tecnología probada (ArcGIS IPS)
- **Programa Educativo Esri:** Pricing especial para instituciones

**Programa Educativo Esri (Colombia):**
- **Small Institution (< 2,500 estudiantes):** 
  - Licencias académicas: Ilimitadas
  - Licencias administrativas: 10
  - ArcGIS Online credits: 500,000 anuales (académico) + 5,000 (administrativo)
  - Soporte técnico: 4 contactos
  - **Costo:** Tarifa anual especial (contactar Esri Colombia)

- **Medium Institution (2,500-10,000 estudiantes):**
  - Licencias académicas: Ilimitadas
  - Licencias administrativas: 20
  - ArcGIS Online credits: 2,000,000 anuales (académico) + 10,000 (administrativo)
  - Soporte técnico: 6 contactos
  - **Costo:** Tarifa anual especial (contactar Esri Colombia)

- **Large Institution (> 10,000 estudiantes):**
  - Licencias académicas: Ilimitadas
  - Licencias administrativas: 100
  - ArcGIS Online credits: 5,000,000 anuales (académico) + 50,000 (administrativo)
  - Soporte técnico: 10 contactos
  - **Costo:** Tarifa anual especial (contactar Esri Colombia)

**Instituciones Colombianas con Programa Esri:**
- Universidad de Los Andes (UASIG)
- Universidad Militar
- Universidad Central
- Universidad Jorge Tadeo Lozano
- Universidad de Antioquia
- Universidad de Manizales
- Universidad San Buenaventura
- Universidad Distrital
- SENA
- Universidad Nacional

**Desventajas:**
- Costo hardware: $1,000-$10,000 USD (50-200 beacons)
- Mantenimiento: Reemplazo de baterías cada 2-3 años
- Calibración compleja (2-4 semanas por edificio)
- Requiere contacto con Esri Colombia para pricing específico

**Viabilidad:** ✅ Alta - Programa educativo hace que sea accesible para instituciones

---

### Opción D: Ultrasonic Positioning

**Descripción:** Beacon ultrasónicos para mayor precisión.

**Ventajas:**
- Precisión: 0.5-1 metro (mayor que Bluetooth)
- Costo: $10-20 por beacon
- No interferencia con Wi-Fi/Bluetooth

**Desventajas:**
- Tecnología menos madura
- Requiere hardware especializado
- Menor ecosistema de herramientas

**Viabilidad:** ⚠️ Baja - Tecnología emergente, riesgo de implementación

---

## Roadmap de Validación Propuesto

### Fase 0: MVP Software (4-6 semanas)

**Objetivo:** Validar concepto sin inversión en hardware.

**Entregables:**
- Mapa 2D básico con Leaflet
- Búsqueda de espacios
- Navegación por waypoints predefinidos
- Accesibilidad WCAG AA
- MVP de voz básico

**Costo:** $0 (desarrollo software puro)

**Métricas de Validación:**
- Adopción por estudiantes
- Satisfacción con navegación básica
- Feedback sobre precisión suficiente

---

### Fase 1: Piloto Wi-Fi Fingerprinting (8-12 semanas)

**Objetivo:** Validar posicionamiento indoor con costo mínimo.

**Entregables:**
- Implementación Wi-Fi fingerprinting
- 1 edificio piloto
- Navegación indoor real
- Comandos de voz avanzados

**Costo:** $0 (software) + calibración (tiempo)

**Métricas de Validación:**
- Precisión de posicionamiento
- Éxito de navegación
- Satisfacción usuarios

---

### Fase 2: Piloto ArcGIS IPS con Programa Educativo (opcional, 8-12 semanas)

**Objetivo:** Validar solución premium con pricing educativo especial si Fase 1 exitosa.

**Entregables:**
- 10-15 beacons en edificio piloto
- Integración ArcGIS IPS con programa educativo Esri
- Tracking en tiempo real
- Blue dot navigation
- Contacto con Esri Colombia para licenciamiento

**Costo:** $500-$1,000 (hardware) + licencia educativa Esri (tarifa anual especial)

**Métricas de Validación:**
- Precisión sub-métrica
- ROI vs costo educativo
- Diferenciación competitiva
- Facilidad de integración con SIGEA

---

## Preguntas de Validación Críticas

### Técnicas
1. ¿Qué nivel de precisión es aceptable para navegación?
2. ¿Es crítico el tracking en tiempo real o basta punto a punto?
3. ¿Qué presupuesto está disponible para hardware?
4. ¿Prefieren solución 100% software o inversión en hardware?

### Funcionales
1. ¿Qué tipo de espacios es prioritario implementar primero?
2. ¿Necesitan sistema de reservas para ciertos espacios?
3. ¿El sistema de citas para oficinas es crítico?
4. ¿Qué metadatos adicionales necesitan por tipo de espacio?

### Usuario
1. ¿Tienen usuarios ciegos para beta testing?
2. ¿Qué nivel de detalle en descripciones auditivas?
3. ¿Necesitan multi-idioma o solo español?
4. ¿Qué porcentaje de estudiantes usará móvil vs desktop?

### Negocio
1. ¿Cuál es el presupuesto total para el proyecto?
2. ¿Qué ROI esperan en 12-18 meses?
3. ¿Están dispuestos a invertir en hardware para diferenciación?
4. ¿Qué timeline tienen para implementación completa?

---

## Estrategia de Implementación por Tiers

### Visión Escalonada del Producto

**SIGEA se implementará en 3 tiers escalonados, permitiendo crecimiento gradual del producto y del mercado:**

**Tier 1: Básico (Inicio)**
- Mapa interactivo 2D (Leaflet)
- Búsqueda de espacios
- Navegación por waypoints
- Accesibilidad WCAG AA
- MVP de voz básico
- **Sin hardware adicional**

**Tier 2: Pro (Crecimiento)**
- Todo Tier 1 +
- Wi-Fi fingerprinting (posicionamiento indoor)
- Navegación indoor real
- Comandos de voz avanzados
- Reportes de ocupación
- **Sin hardware adicional**

**Tier 3: Premium (Liderazgo)**
- Todo Tier 2 +
- ArcGIS IPS con beacons
- Blue dot navigation en tiempo real
- Tracking continuo
- Asistente conversacional avanzado
- **Hardware: beacons + licencia Esri**

---

## Especificaciones por Tier

### Tier 1: Básico (Gratuito - $0/mes)

**Objetivo:** Validación rápida del concepto, adopción inicial del mercado.

**Mapa Interactivo:**
- Mapa 2D con Leaflet (OpenStreetMap)
- Marcadores por tipo de espacio
- Búsqueda de espacios por nombre/tipo
- Información detallada al click
- Filtros por categoría de espacio
- **Sin posicionamiento indoor**

**Accesibilidad:**
- WCAG 2.1 AA compliance
- Screen reader compatibility (NVDA, JAWS, VoiceOver)
- Keyboard navigation completa
- Alto contraste
- Texto escalable al 200%

**Voz (Básico):**
- Web Speech API para comandos básicos
- "Buscar [espacio]"
- "¿Dónde está [espacio]?"
- Feedback auditivo de acciones

**Funcionalidades:**
- Consulta de disponibilidad de espacios
- Horarios de oficinas administrativas
- Agenda docente (si aplica)
- Filtros por sede/edificio/aula

**Tecnología:**
- 100% software (sin hardware)
- Leaflet.js para mapas
- Web Speech API nativa
- Django backend
- Bootstrap frontend

**Target:**
- Instituciones pequeñas (< 2,500 estudiantes)
- Presupuesto limitado
- Validación de concepto
- Adopción inicial

---

### Tier 2: Pro ($50/mes por institución)

**Objetivo:** Diferenciación competitiva con posicionamiento indoor sin hardware costoso.

**Mapa Interactivo:**
- Todo Tier 1 +
- Wi-Fi fingerprinting para posicionamiento indoor
- Navegación indoor real (3-5 metros precisión)
- Rutas paso a paso entre espacios
- Geolocalización indoor del usuario
- Lista de espacios cercanos ordenados por distancia

**Accesibilidad:**
- Todo Tier 1 +
- Exploración auditiva del mapa
- Anuncios de proximidad
- Guía paso a paso por voz
- Feedback sonoro de dirección

**Voz (Avanzado):**
- Todo Tier 1 +
- "Llévame a [espacio]"
- "¿Qué hay cerca?"
- "Explorar mapa"
- Contexto espacial en respuestas

**Funcionalidades:**
- Todo Tier 1 +
- Sistema de citas para oficinas
- Reservas de espacios (canchas, auditorios)
- Reportes de ocupación detallados
- Optimización de espacios

**Tecnología:**
- 100% software (sin hardware)
- Wi-Fi fingerprinting (Cisco CMX / Aruba Meridian / OpenSource)
- Leaflet.js + plugins de routing
- Web Speech API avanzada
- Django backend + API REST

**Target:**
- Instituciones medianas (2,500-10,000 estudiantes)
- Buscan diferenciación sin inversión hardware
- Presupuesto moderado
- Crecimiento del producto

---

### Tier 3: Premium ($200+/mes por institución + costo hardware)

**Objetivo:** Liderazgo del mercado con tecnología de punta y posicionamiento sub-métrico.

**Mapa Interactivo:**
- Todo Tier 2 +
- ArcGIS IPS con beacons Bluetooth
- Blue dot navigation en tiempo real
- Tracking continuo mientras camina
- Precisión sub-métrica (1-3 metros)
- Mapas 2D/3D con planos arquitectónicos

**Accesibilidad:**
- Todo Tier 2 +
- Asistente conversacional avanzado
- Reconocimiento de contexto
- Descripciones espaciales detalladas
- Integración con TTS de alta calidad (Google Cloud TTS)

**Voz (Premium):**
- Todo Tier 2 +
- Asistente conversacional tipo Alexa/Siri
- Preguntas contextuales complejas
- Multi-idioma
- Aprendizaje de preferencias del usuario

**Funcionalidades:**
- Todo Tier 2 +
- API access para integraciones
- Integración con sistemas académicos existentes
- Soporte prioritario
- Customización por institución
- Análisis predictivo de ocupación

**Tecnología:**
- ArcGIS IPS (Programa Educativo Esri)
- Bluetooth beacons ($1,000-$10,000 USD según campus)
- ArcGIS Online integration
- App nativa (iOS/Android) + web
- Machine learning para optimización

**Target:**
- Instituciones grandes (> 10,000 estudiantes)
- Buscan liderazgo tecnológico
- Presupuesto disponible
- Diferenciación competitiva máxima

**Costo Adicional:**
- Hardware: $1,000-$10,000 USD (beacons)
- Licencia Esri: Tarifa anual especial (contactar Esri Colombia)
- Mantenimiento: Reemplazo baterías cada 2-3 años

---

## Roadmap de Implementación por Tiers

### Fase 1: Tier 1 Básico (4-6 semanas)

**Objetivo:** MVP para validación rápida y adopción inicial.

**Entregables:**
- Mapa 2D básico con Leaflet
- Búsqueda de espacios
- Accesibilidad WCAG AA
- Voz básica (Web Speech API)
- Deploy en Render

**Costo:** $0 (desarrollo software puro)

**Métricas de Éxito:**
- Adopción por instituciones piloto
- Satisfacción con mapa básico
- Feedback sobre funcionalidades clave

**Criterio de Escalamiento:**
- Mínimo 5 instituciones adoptando Tier 1
- Feedback positivo sobre mapa básico
- Demanda por posicionamiento indoor

---

### Fase 2: Tier 2 Pro (8-12 semanas)

**Objetivo:** Diferenciación competitiva con Wi-Fi fingerprinting.

**Entregables:**
- Wi-Fi fingerprinting implementation
- Navegación indoor real
- Voz avanzada
- Sistema de citas
- Reportes de ocupación

**Costo:** $0 (software) + calibración (tiempo)

**Métricas de Éxito:**
- Precisión de posicionamiento 3-5 metros
- Éxito de navegación > 90%
- Upsell de Tier 1 a Tier 2 > 30%

**Criterio de Escalamiento:**
- Mínimo 10 instituciones en Tier 2
- ROI positivo del desarrollo
- Demanda por tracking en tiempo real

---

### Fase 3: Tier 3 Premium (8-12 semanas)

**Objetivo:** Liderazgo del mercado con ArcGIS IPS.

**Entregables:**
- Integración ArcGIS IPS
- Implementación beacons en campus piloto
- Blue dot navigation
- Asistente conversacional
- API access

**Costo:** $1,000-$10,000 (hardware) + licencia Esri

**Métricas de Éxito:**
- Precisión sub-métrica < 3 metros
- Upsell de Tier 2 a Tier 3 > 20%
- Diferenciación competitiva clara
- ROI positivo en 12-18 meses

**Criterio de Éxito:**
- Mínimo 3 instituciones grandes en Tier 3
- Posicionamiento como líder del mercado
- Sostenibilidad del modelo de negocio

---

## Estrategia de Monetización

### Modelo de Pricing

**Tier 1: Básico (Gratuito)**
- **Costo:** $0/mes
- **Objetivo:** Adopción masiva, validación de concepto
- **Monetización:** Upsell a Tier 2/3, datos anonimizados (opcional)

**Tier 2: Pro ($50/mes)**
- **Costo:** $50/mes por institución
- **Objetivo:** Diferenciación competitiva, revenue recurrente
- **Incluye:** Todo Tier 1 + Wi-Fi fingerprinting + voz avanzada

**Tier 3: Premium ($200+/mes)**
- **Costo:** $200+/mes por institución + costo hardware
- **Objetivo:** Liderazgo del mercado, revenue premium
- **Incluye:** Todo Tier 2 + ArcGIS IPS + asistente conversacional + API

### Proyección de Revenue

**Año 1 (Fase 1-2):**
- 20 instituciones Tier 1 (gratis)
- 5 instituciones Tier 2 ($50/mes = $250/mes = $3,000/año)
- **Total:** $3,000/año

**Año 2 (Fase 2-3):**
- 50 instituciones Tier 1 (gratis)
- 15 instituciones Tier 2 ($50/mes = $750/mes = $9,000/año)
- 3 instituciones Tier 3 ($200/mes = $600/mes = $7,200/año)
- **Total:** $16,200/año

**Año 3 (Escalamiento):**
- 100 instituciones Tier 1 (gratis)
- 40 instituciones Tier 2 ($50/mes = $2,000/mes = $24,000/año)
- 10 instituciones Tier 3 ($200/mes = $2,000/mes = $24,000/año)
- **Total:** $48,000/año

---

## Criterios de Decisión por Tier

### Implementar Tier 1 (Básico) si:
- Buscan validación rápida del concepto
- Presupuesto limitado o nulo
- Prioridad es adopción inicial del mercado
- Quieren probar antes de invertir

### Implementar Tier 2 (Pro) si:
- Tienen presupuesto moderado ($50/mes)
- Buscan diferenciación competitiva
- Necesitan posicionamiento indoor sin hardware costoso
- Quieren features avanzados de voz

### Implementar Tier 3 (Premium) si:
- Tienen presupuesto disponible ($200+/mes + hardware)
- Buscan liderazgo tecnológico del mercado
- Precisión sub-métrica es crítica
- Diferenciación máxima es prioritaria
- Están dispuestos a invertir en hardware

---

## Próximos Pasos

1. **Desarrollo Tier 1 (Básico)** - 4-6 semanas para MVP
2. **Piloto con 3-5 instituciones** - Validación de concepto
3. **Desarrollo Tier 2 (Pro)** - 8-12 semanas después de validación
4. **Contacto con Esri Colombia** - Para pricing Tier 3 cuando tenga clientes
5. **Desarrollo Tier 3 (Premium)** - 8-12 semanas cuando tenga 10+ clientes Tier 2

---

## Roadmap de Implementación (Actualizado Julio 2026)

### Fase 1: Fundamentos (Completado ✅)
- **Sistema de consulta de aulas** ✅
- **Importación de programación Excel** ✅
- **Gestión de usuarios multi-tenant** ✅
- **Dashboard de módulos** ✅
- **Corrección de errores de importación** ✅
- **Responsive design** ✅

### Fase 2: Expansión de Espacios (En Progreso 🔄)
- **Módulo de Horarios de Oficina** (pendiente)
- **Módulo de Cafetería** (pendiente)
- **Módulo de Otros Espacios** (pendiente)
- **Sistema de citas básico** (pendiente)
- **Tiempo estimado:** 4-6 semanas

### Fase 3: Mapa Interactivo Tier 1 (Planeado 📋)
- **Mapa 2D con Leaflet**
- **Búsqueda de espacios**
- **Accesibilidad WCAG AA**
- **Voz básica**
- **Tiempo estimado:** 4-6 semanas

### Fase 4: Indoor Positioning Tier 2 (Planeado 📋)
- **Wi-Fi fingerprinting**
- **Voz avanzada**
- **Navegación punto a punto**
- **Tiempo estimado:** 6-8 semanas

### Fase 5: ArcGIS IPS Tier 3 (Planeado 📋)
- **Bluetooth beacons**
- **Precisión sub-métrica**
- **Asistente conversacional**
- **API access**
- **Tiempo estimado:** 8-12 semanas

---

## Próximos Pasos Recomendados (Actualizado)

### Prioridad Alta (Inmediato)
1. **Implementar módulo de Horarios de Oficina**
   - Crear modelos para horarios de atención
   - Vista de consulta por docente
   - Sistema de citas básico

2. **Implementar módulo de Cafetería**
   - Crear modelos para horarios de servicio
   - Vista de disponibilidad y capacidad
   - Alertas de aforo

### Prioridad Media (Corto Plazo)
3. **Implementar módulo de Otros Espacios**
   - Canchas deportivas
   - Auditorios
   - Bibliotecas

4. **Mejoras UX/UI existentes**
   - Optimizar dashboard de consulta de aulas
   - Agregar filtros avanzados
   - Mejorar visualización de resultados

### Prioridad Baja (Largo Plazo)
5. **Mapa Interactivo Tier 1**
6. **Indoor Positioning Tier 2**
7. **ArcGIS IPS Tier 3**

---

## Recursos Técnicos

### Stack Tecnológico Actual
- **Backend:** Django 4.x
- **Frontend:** Bootstrap 5, HTML/CSS/JavaScript
- **Base de Datos:** PostgreSQL
- **Hosting:** Render
- **Multi-tenancy:** Sistema custom con aislamiento por institución

### Archivos Principales
- `proyectos/views.py` - Vistas principales
- `proyectos/models.py` - Modelos de datos
- `proyectos/services/excel_importer.py` - Importación de Excel
- `proyectos/templates/dashboard_modulos.html` - Dashboard de módulos
- `proyectos/urls.py` - Configuración de URLs

### Comandos Útiles
```bash
# Deploy en Render
git push origin main

# Logs en Render
https://dashboard.render.com -> Logs

# Acceso a producción
https://sigea-pilot.onrender.com
```

---

## Contacto y Soporte

**Desarrollador:** Equipo SIGEA
**Fecha de última actualización:** Julio 2026
**Versión del sistema:** 1.2 (con dashboard de módulos y correcciones)

---

*Documento para validación con cliente antes de iniciar desarrollo*
*Fecha: Julio 2026*
*Versión: 2.1 - Con estado actual y roadmap actualizado*
