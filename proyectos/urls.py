from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import mapa_views

urlpatterns = [

    path(
        'acceso/',
        auth_views.LoginView.as_view(template_name='acceso.html', redirect_authenticated_user=True),
        name='login'
    ),
    path('salir/', auth_views.LogoutView.as_view(), name='logout'),

    path(
        "",
        views.dashboard_modulos,
        name="dashboard_modulos"
    ),

    path(
        "consultar-aulas/",
        views.aulas_disponibles,
        name="consulta_aulas"
    ),

    path(
        "mapa/",
        mapa_views.mapa_interactivo,
        name="mapa_interactivo"
    ),

    path(
        "mapa/api/<int:edificio_id>/",
        mapa_views.api_estado_plano,
        name="api_estado_plano"
    ),

    path(
        "conflictos/",
        views.reporte_conflictos,
        name="reporte_conflictos"
    ),

    path(
        "conflictos/reasignar/<int:clase_id>/<int:aula_id>/",
        views.asignar_aula_alternativa,
        name="asignar_aula_alternativa"
    ),

    path(
        "agenda-docente/<int:docente_id>/",
        views.agenda_docente,
        name="agenda_docente"
    ),

    path(
        "dashboard-reportes/",
        views.dashboard_reportes,
        name="dashboard_reportes"
    ),

    # -----------------------
    # AJAX
    # -----------------------

    path(
        "obtener-edificios/",
        views.obtener_edificios,
        name="obtener_edificios"
    ),

    path(
        "obtener-aulas/",
        views.obtener_aulas,
        name="obtener_aulas"
    ),

]
