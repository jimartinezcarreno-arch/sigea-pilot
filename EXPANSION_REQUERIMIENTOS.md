# SIGEA - Expansión de Requerimientos del Cliente

## Visión Expandida del Producto

**SIGEA evoluciona de "Sistema de Gestión de Espacios Académicos" a "Sistema Integral de Gestión de Espacios Físicos"**

La plataforma debe gestionar TODOS los espacios físicos de una institución educativa, no solo aulas académicas, permitiendo:

- **Optimización administrativa** de toda la infraestructura
- **Consulta pública** para estudiantes y docentes
- **Gestión interna** para administrativos
- **Mapa interactivo** completo del campus

---

## Nuevos Tipos de Espacios a Gestionar

### 1. Espacios Académicos (Ya implementados)
- ✅ Aulas de clase
- ✅ Laboratorios de informática
- ✅ Auditorios
- ✅ Salones de conferencias

### 2. Espacios Administrativos (Nuevos)
- 📋 **Oficinas administrativas**
  - Rectoría, Vicerrectorías
  - Secretarías académicas
  - Finanzas, Recursos Humanos
  - Bienestar estudiantil
  
- 📋 **Horarios de oficina**
  - Horarios de atención al público
  - Disponibilidad de funcionarios
  - Citas y agendamientos

### 3. Espacios de Servicios (Nuevos)
- 🍽️ **Cafeterías y comedores**
  - Horarios de servicio
  - Capacidad de aforo
  - Menús del día (opcional)

- 🏃 **Canchas deportivas**
  - Canchas de fútbol, baloncesto, voleibol
  - Horarios de uso
  - Reservas para actividades

- 📚 **Bibliotecas y salas de estudio**
  - Zonas de estudio individual/grupal
  - Horarios de apertura
  - Disponibilidad de cubículos

### 4. Espacios Complementarios (Nuevos)
- 🚗 **Parqueaderos**
  - Zonas de estacionamiento
  - Disponibilidad de cupos
  - Tarifas (opcional)

- 🌳 **Zonas verdes y recreativas**
  - Jardines, plazas
  - Áreas de descanso
  - Espacios para eventos

- 🏥 **Puntos de atención médica**
  - Enfermería
  - Consultorios médicos
  - Horarios de atención

---

## Funcionalidades por Rol de Usuario

### 👨‍🎓 Estudiantes
**Objetivo:** Consultar información pública sin autenticación

**Funcionalidades:**
- 🗺️ **Mapa interactivo del campus**
  - Ubicar su aula de clase actual
  - Encontrar oficinas administrativas
  - Localizar servicios (cafetería, biblioteca, etc.)
  - Rutas de navegación entre espacios

- 📅 **Consulta de horarios**
  - Ver su horario de clases
  - Consultar disponibilidad de espacios
  - Horarios de atención de oficinas

- 🔍 **Búsqueda de espacios**
  - Buscar por tipo de espacio
  - Filtrar por ubicación/sede
  - Ver información detallada (capacidad, recursos)

### 👨‍🏫 Docentes
**Objetivo:** Gestionar su agenda y consultar espacios

**Funcionalidades:**
- ✅ **Agenda docente** (ya implementada)
  - Ver su horario de clases completo
  - Consultar disponibilidad de aulas
  - Filtrar por periodo

- 📋 **Horarios de oficina**
  - Definir sus horarios de atención
  - Gestionar citas con estudiantes
  - Ver disponibilidad de su oficina

- 🗺️ **Mapa interactivo**
  - Ubicar sus aulas asignadas
  - Encontrar oficinas administrativas
  - Planificar rutas entre clases

- 📊 **Reportes de uso**
  - Estadísticas de ocupación de sus clases
  - Historial de asignaciones

### 👔 Administrativos
**Objetivo:** Gestionar todos los espacios físicos

**Funcionalidades:**
- 🏢 **Gestión de espacios**
  - Crear/editar todos los tipos de espacios
  - Definir capacidades y recursos
  - Asignar horarios de disponibilidad
  - Gestionar mantenimiento

- 👥 **Gestión de horarios de oficina**
  - Definir horarios de atención
  - Asignar funcionarios a espacios
  - Gestionar citas y agendamientos
  - Reportes de atención

- 📊 **Optimización de espacios**
  - Análisis de ocupación por tipo de espacio
  - Detección de espacios subutilizados
  - Recomendaciones de reasignación
  - Costos por metro cuadrado

- 🔧 **Configuración institucional**
  - Definir tipos de espacios personalizados
  - Configurar reglas de uso
  - Gestionar permisos y accesos
  - Integración con sistemas externos

---

## Mapa Interactivo Completo con Indoor Positioning

### Visión: Sistema de Navegación Indoor tipo ArcGIS IPS

**Referencia:** ArcGIS IPS en ETH Zurich - Sistema de posicionamiento indoor con "blue dot" en tiempo real

### Características del Mapa Avanzado

**1. Indoor Positioning System (IPS)**
- 📍 **Blue Dot en tiempo real** - Punto azul que muestra ubicación exacta del usuario
- 🏢 **Navegación indoor** - Funciona dentro de edificios (sin GPS)
- 🔄 **Tracking continuo** - Seguimiento en tiempo real mientras camina
- 🎯 **Precisión sub-métrica** - Ubicación precisa dentro de 1-3 metros
- 📱 **Multi-plataforma** - Funciona en iOS, Android y web

**2. Visualización de Espacios**
- 🗺️ **Mapa 2D/3D** del campus completo con planos arquitectónicos
- 📍 **Marcadores** por tipo de espacio con colores y animaciones
- 🔍 **Zoom y navegación** intuitiva con gestos táctiles
- 📱 **Responsivo** para móviles y tablets
- 🌙 **Modo oscuro/claro** para accesibilidad

**3. Tipos de Marcadores con Animaciones**
- 🟢 **Aulas** (verde) - Pulso cuando están libres
- 🔵 **Oficinas** (azul) - Icono de persona cuando hay funcionario
- 🟡 **Servicios** (amarillo) - Animación de horario activo
- 🔴 **Deportivos** (rojo) - Icono de actividad cuando en uso
- 🟣 **Culturales** (morado) - Efecto de brillo para eventos
- ⚪ **Otros** (blanco) - Marcador estándar

**4. Información al Click + Voice Feedback**
- Nombre del espacio (leído por voz)
- Tipo y capacidad (anunciado auditivamente)
- Horarios de disponibilidad (descripción vocal)
- Funcionarios asignados (oficinas)
- Recursos disponibles
- Estado actual (ocupado/libre) con feedback sonoro

**5. Funcionalidades Avanzadas**
- 🧭 **Rutas de navegación** entre espacios con instrucciones paso a paso
- 🔍 **Búsqueda visual** en el mapa con resultados destacados
- 📍 **Geolocalización indoor** del usuario en tiempo real
- 📋 **Lista de espacios cercanos** ordenados por distancia
- 🎯 **Filtros por tipo de espacio** con accesibilidad
- 🗣️ **Comandos de voz** para navegación manos libres

---

## Sistema de Accesibilidad por Voz

### Visión: SIGEA 100% Accesible para Personas con Discapacidad Visual

**Principio:** La accesibilidad no es una característica adicional, es un derecho fundamental. SIGEA debe ser completamente navegable sin visión.

### Tecnologías de Accesibilidad

**1. Web Speech API (Nativo del navegador)**
- 🗣️ **Speech Recognition** - Reconocimiento de voz para comandos
- 🔊 **Speech Synthesis** - Síntesis de voz para respuestas
- 🌍 **Multi-idioma** - Español, inglés, portugués, etc.
- 📱 **Sin dependencias externas** - Funciona nativamente en navegadores modernos

**2. Screen Reader Integration**
- 🎧 **NVDA, JAWS, VoiceOver** - Compatibilidad total con lectores de pantalla
- 🏷️ **ARIA labels** - Etiquetas semánticas para accesibilidad
- 📋 **Live regions** - Anuncios dinámicos de cambios
- ⌨️ **Keyboard navigation** - Navegación completa por teclado

**3. Voice Commands Avanzados**
```javascript
// Ejemplo de comandos de voz
"Llévame a la cafetería" → Navegación automática
"¿Dónde está mi próxima clase?" → Búsqueda y ruta
"¿Qué oficinas están cerca?" → Lista de espacios cercanos
"Explorar mapa" → Modo de exploración auditiva
"Detener navegación" → Cancelar ruta actual
```

### Funcionalidades de Accesibilidad

**1. Exploración Auditiva del Mapa**
- 🔊 **Descripción espacial** - "A tu izquierda hay una oficina de rectoría"
- 📢 **Anuncios de proximidad** - "Estás a 5 metros de la cafetería"
- 🧭 **Guía paso a paso** - "Gira a la derecha, camina 10 metros"
- 🎯 **Feedback de destino** - "Has llegado a tu destino"

**2. Interacción por Voz**
- 🗣️ **Búsqueda de espacios** - "Buscar biblioteca"
- 📅 **Consulta de horarios** - "¿Cuándo abre la cafetería?"
- 🔄 **Navegación manos libres** - "Llévame a mi clase"
- ❓ **Preguntas contextuales** - "¿Qué hay aquí?"

**3. Feedback Sonoro**
- 🔔 **Alertas de proximidad** - Sonidos al acercarse a destino
- 🎵 **Indicadores de dirección** - Tono cambia según dirección
- ⚠️ **Advertencias de obstáculos** - "Cuidado, escaleras adelante"
- ✅ **Confirmaciones** - Sonidos de éxito al llegar

**4. Modo Alto Contraste**
- 🌗 **Colores WCAG AA/AAA** - Contraste mínimo 4.5:1
- 🖼️ **Iconos grandes** - Mínimo 44x44 píxeles
- 📝 **Texto legible** - Fuente mínima 16px, escalable al 200%
- 🎨 **Sin dependencia de color** - Información redundante

### Implementación Técnica

**1. Web Speech API Integration**
```javascript
// Speech Recognition
const recognition = new webkitSpeechRecognition();
recognition.lang = 'es-ES';
recognition.continuous = true;
recognition.interimResults = true;

// Speech Synthesis
const synthesis = window.speechSynthesis;
const utterance = new SpeechSynthesisUtterance("Texto a leer");
utterance.lang = 'es-ES';
utterance.rate = 1.0; // Velocidad normal
utterance.pitch = 1.0; // Tono normal
```

**2. ARIA Labels Semánticos**
```html
<button aria-label="Buscar espacio" aria-describedby="search-help">
  <i class="icon-search"></i>
</button>
<div id="search-help" class="sr-only">
  Presiona para buscar espacios en el mapa
</div>
```

**3. Live Regions para Anuncios Dinámicos**
```html
<div aria-live="polite" aria-atomic="true" id="announcer">
  <!-- Anuncios de cambios en el mapa -->
</div>
```

---

## Análisis Técnico y Propuestas de Mejora

### Punto de Vista: Evaluación Crítica de la Propuesta

#### 🎯 Fortalezas del Diseño Propuesto

**1. Visión Integral y Escalable**
- La expansión de SIGEA de "aulas" a "todos los espacios" es estratégicamente correcta
- Permite monetización adicional (SaaS premium)
- Diferenciación competitiva clara vs soluciones académicas tradicionales

**2. Enfoque en Accesibilidad**
- La inclusión de voz para discapacidad visual es innovadora
- Cumple con estándares WCAG 2.1 AA/AAA
- Mercado desatendido con alto impacto social

**3. Tecnología Indoor Positioning**
- ArcGIS IPS es la solución líder del mercado
- Precisión sub-métrica es realista con hardware adecuado
- Experiencia usuario similar a Google Maps indoor

#### ⚠️ Desafíos Técnicos Críticos

**1. Costo de Implementación IPS**
- **Hardware requerido:** Beacons Bluetooth LE ($20-50 cada uno)
- **Infraestructura:** 1 beacon cada 10-15 metros para precisión óptima
- **Campus típico:** 50-200 beacons = $1,000-$10,000 USD
- **Mantenimiento:** Reemplazo de baterías cada 2-3 años

**2. Calibración Compleja**
- **Fingerprinting:** Requiere mapeo inicial de cada edificio
- **Tiempo:** 2-4 semanas por edificio grande
- **Personal especializado:** Ingenieros GIS + técnicos de redes
- **Actualizaciones:** Recalibración cuando cambia la infraestructura

**3. Dependencia de Hardware**
- **iOS:** Limitaciones de Bluetooth en background
- **Android:** Fragmentación de hardware y versiones
- **Web:** Acceso limitado a Bluetooth en navegadores
- **Solución híbrida:** App nativa + web fallback

**4. Costos de Licencias**
- **ArcGIS IPS:** Licensing por edificio/usuario
- **Alternativas:** Mapbox Indoor, IndoorAtlas (más económicos)
- **Open source:** Proyectos como IndoorJS (menos maduros)

#### 💡 Propuestas de Mejora Estratégicas

**1. Enfoque Fásico para Reducir Riesgo**

**Fase 0: MVP Indoor (4-6 semanas)**
- Implementar mapa 2D básico sin IPS
- QR codes en puntos clave para "check-in"
- Navegación basada en waypoints predefinidos
- Costo: $0 (software puro)

**Fase 1: IPS Piloto (8-12 semanas)**
- Implementar IPS en 1 edificio piloto
- 10-15 beacons para proof of concept
- Validar precisión y UX
- Costo: $500-$1,000 (hardware) + licencias

**Fase 2: Expansión Gradual (6-12 meses)**
- Escalar a edificios de alto tráfico
- Priorizar cafeterías, bibliotecas, auditorios
- Costo escalonado según ROI

**2. Alternativas Tecnológicas Costo-Efectivas**

**Opción A: Wi-Fi Fingerprinting**
- **Ventaja:** Usa infraestructura Wi-Fi existente
- **Precisión:** 3-5 metros (aceptable para navegación)
- **Costo:** $0 (software puro)
- **Herramientas:** Cisco CMX, Aruba Meridian

**Opción B: QR Codes + GPS Híbrido**
- **Ventaja:** QR codes en puntos clave + GPS outdoor
- **Precisión:** 1-2 metros (en puntos QR)
- **Costo:** $50-100 (impresión de QR codes)
- **UX:** Escanear QR para ubicación precisa

**Opción C: Ultrasonic Positioning**
- **Ventaja:** Mayor precisión que Bluetooth
- **Precisión:** 0.5-1 metro
- **Costo:** $10-20 por beacon
- **Herramientas:** Dolphin, Sonitor

**3. Arquitectura de Accesibilidad Robusta**

**Capa 1: Base (WCAG 2.1 AA)**
- HTML semántico, ARIA labels, keyboard navigation
- Screen reader compatibility
- Alto contraste, texto escalable

**Capa 2: Voz (Web Speech API)**
- Comandos básicos de navegación
- Feedback auditivo de acciones
- Multi-idioma

**Capa 3: Avanzado (Opcional)**
- Reconocimiento de contexto
- Asistente conversacional
- Integración con TTS de alta calidad (Google Cloud TTS)

**4. Monetización Estratégica**

**Tier Básico (Gratuito)**
- Mapa 2D básico
- Búsqueda de espacios
- Accesibilidad WCAG AA

**Tier Pro ($50/mes)**
- Indoor positioning (1 edificio)
- Comandos de voz básicos
- Reportes de ocupación

**Tier Enterprise ($200+/mes)**
- IPS completo (todos los edificios)
- Asistente conversacional avanzado
- API access, integraciones
- Soporte prioritario

#### 🚀 Roadmap Técnico Optimizado

**Mes 1-2: Fundamentos**
- Modelo de datos expandido
- Mapa 2D básico con Leaflet
- Accesibilidad WCAG AA
- MVP de voz básico

**Mes 3-4: IPS Piloto**
- Implementación Wi-Fi fingerprinting
- 1 edificio piloto
- Validación de precisión
- Feedback de usuarios

**Mes 5-6: Escalado**
- Expansión a 3-5 edificios
- Comandos de voz avanzados
- Integración con sistemas existentes
- Beta testing con usuarios ciegos

**Mes 7-12: Producción**
- Despliegue completo
- Optimización de performance
- Marketing y ventas
- Soporte continuo

#### 📊 Métricas de Éxito

**Técnicas**
- Precisión de posicionamiento: < 3 metros
- Tiempo de respuesta voz: < 500ms
- Uptime: 99.9%
- Compatibilidad: iOS 12+, Android 8+, Chrome 90+

**Usuario**
- Tasa de éxito de navegación: > 95%
- Satisfacción usuarios ciegos: > 4/5
- Reducción de tiempo de búsqueda: > 50%
- Adopción: > 60% de estudiantes

**Negocio**
- ROI positivo en 12-18 meses
- Retención: > 80%
- Expansión a nuevas instituciones
- Upsell a tier Enterprise: > 20%

---

## Horarios de Oficina Administrativa

### Modelo de Datos

**Nuevas Entidades:**
```python
class HorarioOficina(models.Model):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    dia_semana = models.IntegerField()  # 1-7
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)

class Cita(models.Model):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(choices=['PENDIENTE', 'CONFIRMADA', 'CANCELADA'])
```

### Funcionalidades

**1. Definición de Horarios**
- Administrativos definen horarios de atención
- Asignación de funcionarios a espacios
- Configuración de breaks y excepciones

**2. Consulta Pública**
- Estudiantes pueden ver horarios de atención
- Filtrado por tipo de trámite
- Información de documentos requeridos

**3. Sistema de Citas**
- Estudiantes solicitan citas online
- Confirmación automática por email
- Recordatorios de citas
- Gestión de cancelaciones

---

## Impacto en Arquitectura Actual

### Cambios en Modelos

**1. Modelo Espacio (Expansión)**
```python
class Espacio(models.Model):
    # Campos existentes
    nombre = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    tipo_espacio = models.CharField(max_length=50)
    
    # Nuevos campos
    categoria = models.CharField(  # ACADEMICO, ADMINISTRATIVO, SERVICIO, DEPORTIVO
        choices=['ACADEMICO', 'ADMINISTRATIVO', 'SERVICIO', 'DEPORTIVO', 'COMPLEMENTARIO']
    )
    coordenadas_x = models.FloatField(null=True)  # Para mapa
    coordenadas_y = models.FloatField(null=True)  # Para mapa
    piso = models.IntegerField(null=True)
    horario_apertura = models.TimeField(null=True)
    horario_cierre = models.TimeField(null=True)
    requiere_reserva = models.BooleanField(default=False)
    costo_hora = models.DecimalField(null=True, decimal_places=2)
```

**2. Nuevos Modelos**
- `Funcionario` (para oficinas administrativas)
- `Estudiante` (para agendamiento de citas)
- `HorarioOficina`
- `Cita`
- `ReservaEspacio` (para canchas, auditorios, etc.)

### Cambios en Vistas

**1. Nuevas Vistas**
- `mapa_interactivo_completo` - Mapa con todos los espacios
- `horarios_oficina` - Consulta de horarios administrativos
- `agendar_cita` - Sistema de citas
- `gestion_espacios_admin` - CRUD de todos los espacios
- `reportes_ocupacion_general` - Análisis por tipo de espacio

**2. Vistas Modificadas**
- `aulas_disponibles` → `espacios_disponibles` (generalizar)
- `mapa_interactivo` → Incluir todos los tipos de espacios

### Cambios en Frontend

**1. Componentes Nuevos**
- Mapa interactivo con Leaflet/Mapbox
- Filtros por tipo de espacio
- Panel lateral con información detallada
- Sistema de rutas entre puntos

**2. Componentes Modificados**
- Dashboard principal → Incluir selector de tipo de espacio
- Filtros rápidos → Agregar filtros por categoría

---

## Priorización de Features

### Fase 1: Fundacional (4-6 semanas)
**Objetivo:** Expandir modelo de datos y mapa básico

1. ✅ **Expansión del modelo Espacio**
   - Agregar categoría y coordenadas
   - Migración de datos existentes

2. ✅ **Mapa interactivo básico**
   - Integración con Leaflet
   - Visualización de todos los espacios
   - Marcadores por tipo

3. ✅ **Horarios de oficina**
   - Modelo HorarioOficina
   - CRUD de horarios
   - Consulta pública

### Fase 2: Funcionalidad Core (6-8 semanas)
**Objetivo:** Implementar funcionalidades principales

4. ✅ **Sistema de citas**
   - Modelo Cita
   - Flujo de solicitud
   - Confirmación y recordatorios

5. ✅ **Gestión de espacios completa**
   - CRUD para todos los tipos
   - Validaciones por categoría
   - Reglas de uso

6. ✅ **Reportes ampliados**
   - Análisis por tipo de espacio
   - Métricas de ocupación general
   - Costos y optimización

### Fase 3: Experiencia de Usuario (4-6 semanas)
**Objetivo:** Mejorar UX para estudiantes y docentes

7. ✅ **Mapa avanzado**
   - Rutas de navegación
   - Geolocalización
   - Búsqueda visual

8. ✅ **App móvil** (opcional)
   - Versión móvil optimizada
   - Notificaciones push
   - Offline mode

9. ✅ **Integraciones**
   - SSO institucional
   - Sistemas académicos existentes
   - Pasarelas de pago (reservas)

---

## Beneficios del SaaS Expandido

### Para Instituciones
- 🏢 **Optimización completa** de infraestructura
- 💰 **Reducción de costos** por mejor uso de espacios
- 📊 **Data-driven decisions** sobre expansión
- 🎯 **Mejor servicio** a estudiantes y docentes

### Para Estudiantes
- 🗺️ **Fácil navegación** por el campus
- 📅 **Horarios claros** de atención
- 📱 **Acceso móvil** a información
- ⏰ **Ahorro de tiempo** en trámites

### Para Docentes
- 📋 **Gestión centralizada** de agenda
- 🏢 **Visión completa** de espacios disponibles
- 📊 **Métricas de uso** de sus clases
- 🎯 **Mejor planificación** de actividades

### Para Administrativos
- 🔧 **Control total** de espacios físicos
- 📈 **Análisis detallado** de ocupación
- 💡 **Optimización** de recursos
- 🚀 **Escalabilidad** del sistema

---

## Consideraciones Técnicas

### Performance
- **Caching** de mapas y coordenadas
- **Indexación** de espacios por tipo y ubicación
- **Lazy loading** de marcadores en mapa
- **CDN** para assets estáticos

### Escalabilidad
- **Base de datos** optimizada para consultas geoespaciales
- **Microservicios** para cálculo de rutas (opcional)
- **Balanceo de carga** para alta concurrencia

### Seguridad
- **RBAC** granular por tipo de espacio
- **Audit logs** de cambios en espacios
- **Rate limiting** para API pública
- **Sanitización** de coordenadas y datos geoespaciales

---

## Roadmap Resumido

| Fase | Duración | Features Clave | Impacto |
|------|----------|----------------|---------|
| 1 | 4-6 semanas | Modelo expandido, mapa básico, horarios oficina | Fundacional |
| 2 | 6-8 semanas | Sistema de citas, gestión espacios, reportes | Core |
| 3 | 4-6 semanas | Mapa avanzado, app móvil, integraciones | UX |

**Total estimado:** 14-20 semanas para transformación completa

---

## Validación con Cliente

### Preguntas Clave para Validación:

1. **Prioridades:** ¿Qué tipo de espacios es más urgente implementar primero?

2. **Mapa:** ¿Prefieren mapa 2D o 3D? ¿Necesitan rutas de navegación?

3. **Citas:** ¿El sistema de citas es prioritario o puede ser fase posterior?

4. **Móvil:** ¿Es crítico tener app móvil o basta versión web responsiva?

5. **Integraciones:** ¿Qué sistemas existentes deben integrarse (SIS, ERP, etc.)?

6. **Presupuesto:** ¿Cuál es el presupuesto y timeline esperado para esta expansión?

7. **Usuarios:** ¿Cuántos usuarios concurrentes esperan (estudiantes, docentes, admin)?

---

*Documento creado para validación con cliente antes de iniciar desarrollo*
*Fecha: Julio 2026*
*Versión: 1.0 - Propuesta de Expansión*
