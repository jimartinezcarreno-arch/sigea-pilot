from django.db import models
from django.core.exceptions import ValidationError
from .tenant_utils import get_current_institucion

# ----------------------------------------------------------------------
# 1. MANAGER PARA MULTI-TENANCY (AISLAMIENTO LÓGICO)
# ----------------------------------------------------------------------
class TenantManager(models.Manager):
    """
    Filtra automáticamente todas las consultas agregando WHERE institucion_id = X
    basado en el contexto de la solicitud HTTP activa.
    """
    def get_queryset(self):
        institucion_activa = get_current_institucion()
        queryset = super().get_queryset()
        if institucion_activa:
            return queryset.filter(institucion=institucion_activa)
        # En un host sin instituciÃ³n reconocida, nunca se deben exponer datos de otra entidad.
        return queryset.none()

class TenantModel(models.Model):
    """
    Clase abstracta de la que deben heredar todos los modelos que requieran
    aislamiento multi-tenant en el sistema.
    """
    institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)
    
    objects = TenantManager()       # Manager filtrado por seguridad
    unfiltered = models.Manager()   # Para tareas globales de sistema (ej. comandos de consola)

    class Meta:
        abstract = True

# ----------------------------------------------------------------------
# 2. MODELO PRINCIPAL (SISTEMA CENTRAL)
# ----------------------------------------------------------------------
class Institucion(models.Model):
    nombre = models.CharField(max_length=255)
    subdominio = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    hora_inicio_jornada = models.TimeField()
    hora_fin_jornada = models.TimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class PerfilUsuario(models.Model):
    """Vincula cada cuenta de acceso con una Ãºnica instituciÃ³n del piloto."""
    ROL_CHOICES = [
        ('ADMIN', 'Administrador institucional'),
        ('PROGRAMADOR', 'Programador académico'),
        ('CONSULTA', 'Consulta'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='perfil_sigea')
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='usuarios')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='CONSULTA')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_username()} - {self.institucion.nombre}"

# ----------------------------------------------------------------------
# 3. ESTRUCTURA ACADÉMICA DINÁMICA (SOLUCIÓN UNIMINUTO)
# ----------------------------------------------------------------------
class ModalidadAcademica(TenantModel):
    """
    Ejemplos: 'Pregrado Semestral Presencial', 'Pregrado Cuatrimestral Dist',
    'Intersemestrales', 'Cursos Libres'.
    """
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class PeriodoAcademico(TenantModel):
    """
    Representa el bloque macro del año escolar asociado a una modalidad.
    Códigos exactos de la tabla institucional: '10', '40', '60', '45', '50', '30', etc.
    """
    modalidad = models.ForeignKey(ModalidadAcademica, on_delete=models.CASCADE, related_name='periodos')
    codigo_institucional = models.CharField(max_length=20) # Mapeo directo con Banner/Génesis
    nombre = models.CharField(max_length=100)            # Ej: "2026-10 (Semestral)" o "2026-40"
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.codigo_institucional}] {self.nombre}"

class MomentoAcademico(models.Model):
    """
    Subdivisiones del periodo académico. Elimina las columnas fijas RT1 y RT2.
    Ejemplos: 'Momento 1', 'Momento 2', 'Periodo Completo'.
    """
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE, related_name='momentos')
    nombre = models.CharField(max_length=100) # Ej: "Momento 1", "Momento 2", "Completo"
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def clean(self):
        # Regla de Negocio: Las fechas del momento deben estar dentro del rango del Periodo Macro
        if self.fecha_inicio < self.periodo.fecha_inicio or self.fecha_fin > self.periodo.fecha_fin:
            raise ValidationError("Las fechas del momento deben estar contenidas dentro del Periodo Académico macro.")
        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

    def __str__(self):
        return f"{self.periodo.nombre} - {self.nombre}"

# ----------------------------------------------------------------------
# 4. INFRAESTRUCTURA FÍSICA Y PERSONAL
# ----------------------------------------------------------------------
class Docente(TenantModel):
    nombre = models.CharField(max_length=255)
    identificacion = models.CharField(max_length=50)
    email = models.EmailField()
    foto = models.ImageField(upload_to='docentes/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Sede(TenantModel):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre

class Edificio(TenantModel):
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='edificios')
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre} ({self.sede.nombre})"

class Aula(TenantModel):
    TIPO_ESPACIO_CHOICES = [
        ('AULA', 'Aula de Clase Ordinaria'),
        ('LAB', 'Laboratorio Especializado'),
        ('AUD', 'Auditorio'),
        ('SALA', 'Sala de Cómputo'),
    ]
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name='aulas')
    nombre = models.CharField(max_length=100) # Ej: "Aula 106"
    capacidad = models.IntegerField()
    tipo_espacio = models.CharField(max_length=10, choices=TIPO_ESPACIO_CHOICES)
    dimensiones_m2 = models.FloatField(blank=True, null=True)
    recursos = models.JSONField(default=dict, blank=True) # Almacena proyectores, aire acondicionado, etc.
    svg_x = models.FloatField(blank=True, null=True, help_text="Posición X en SVG")
    svg_y = models.FloatField(blank=True, null=True, help_text="Posición Y en SVG")
    svg_width = models.FloatField(blank=True, null=True, help_text="Ancho SVG")
    svg_height = models.FloatField(blank=True, null=True, help_text="Alto SVG")

    def __str__(self):
        return f"{self.nombre} - {self.edificio.nombre}"

# ----------------------------------------------------------------------
# 5. PROGRAMACIÓN Y HORARIOS
# ----------------------------------------------------------------------
class Clase(TenantModel):
    DIA_CHOICES = [
        (1, 'Lunes'), (2, 'Martes'), (3, 'Miércoles'),
        (4, 'Jueves'), (5, 'Viernes'), (6, 'Sábado'), (7, 'Domingo'),
    ]
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='clases')
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='clases')
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    momento = models.ForeignKey(MomentoAcademico, on_delete=models.CASCADE, related_name='clases')
    
    asignatura = models.CharField(max_length=255)
    nrc = models.CharField(max_length=20) # Código del curso único en UNIMINUTO
    
    dia_semana = models.IntegerField(choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def clean(self):
        # 1. Validar rangos de jornada institucionales antes de guardar
        institucion_activa = get_current_institucion()
        if institucion_activa:
            if self.hora_inicio < institucion_activa.hora_inicio_jornada or self.hora_fin > institucion_activa.hora_fin_jornada:
                raise ValidationError("La clase excede los límites de la jornada configurada por la institución.")

    def __str__(self):
        return f"{self.asignatura} ({self.nrc}) - {self.aula.nombre}"

    class Meta:
        indexes = [
            models.Index(
                fields=['institucion', 'aula', 'dia_semana', 'hora_inicio', 'hora_fin'],
                name='clase_ins_aula_horario_idx',
            ),
            models.Index(
                fields=['institucion', 'docente', 'dia_semana'],
                name='clase_ins_docente_dia_idx',
            ),
        ]


class ImportacionProgramacion(TenantModel):
    """Audita una carga exitosa y conserva el estado anterior de la programación."""
    TIPO_CHOICES = [
        ('IMPORTACION', 'Importación de Excel'),
        ('RESTAURACION', 'Restauración de historial'),
    ]

    archivo_nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='IMPORTACION')
    creado_por = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='importaciones_sigea'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total_clases = models.PositiveIntegerField(default=0)
    respaldo_anterior = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.archivo_nombre} - {self.fecha_creacion:%Y-%m-%d %H:%M}"
