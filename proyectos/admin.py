from django.contrib import admin
from .models import (
    Institucion, PerfilUsuario, ModalidadAcademica, PeriodoAcademico,
    MomentoAcademico, Docente, Sede, Edificio, Aula, Clase
)

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'subdominio', 'activo')
    search_fields = ('nombre', 'subdominio')

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'institucion', 'rol', 'activo')
    list_filter = ('institucion', 'rol', 'activo')
    search_fields = ('user__username', 'user__email')

@admin.register(ModalidadAcademica)
class ModalidadAcademicaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'institucion')
    list_filter = ('institucion',)

class MomentoAcademicoInline(admin.TabularInline):
    model = MomentoAcademico
    extra = 1

@admin.register(PeriodoAcademico)
class PeriodoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('codigo_institucional', 'nombre', 'modalidad', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('modalidad', 'activo')
    search_fields = ('nombre', 'codigo_institucional')
    inlines = [MomentoAcademicoInline] # Permite crear los momentos directamente dentro del periodo macro

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'identificacion', 'email')
    search_fields = ('nombre', 'identificacion')

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion')

@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sede')
    list_filter = ('sede',)

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edificio', 'tipo_space', 'capacidad')
    list_filter = ('edificio', 'tipo_espacio')
    
    # Un pequeño ajuste por si escribí mal el campo antes
    def tipo_space(self, obj):
        return obj.get_tipo_espacio_display()
    tipo_space.short_description = 'Tipo de Espacio'

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('asignatura', 'nrc', 'docente', 'aula', 'momento', 'dia_semana', 'hora_inicio', 'hora_fin')
    list_filter = ('periodo', 'momento', 'dia_semana', 'aula__edificio')
    search_fields = ('asignatura', 'nrc', 'docente__nombre')
