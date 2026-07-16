import os
from datetime import date, time
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from openpyxl import Workbook

from .models import Aula, Clase, Docente, Edificio, Institucion, ModalidadAcademica, MomentoAcademico, PerfilUsuario, PeriodoAcademico, Sede
from .services.excel_importer import ExcelImporter
from .tenant_utils import set_current_institucion


@override_settings(ALLOWED_HOSTS=["testserver", "inst1.localhost", "unknown.localhost"])
class SIGEATestCase(TestCase):
    def setUp(self):
        self.inst1 = Institucion.objects.create(
            nombre="Institucion Uno", subdominio="inst1",
            hora_inicio_jornada=time(6, 0), hora_fin_jornada=time(22, 0),
        )
        self.inst2 = Institucion.objects.create(
            nombre="Institucion Dos", subdominio="inst2",
            hora_inicio_jornada=time(6, 0), hora_fin_jornada=time(22, 0),
        )
        set_current_institucion(self.inst1)
        modalidad = ModalidadAcademica.objects.create(institucion=self.inst1, nombre="Pregrado")
        periodo = PeriodoAcademico.objects.create(
            institucion=self.inst1, modalidad=modalidad, codigo_institucional="2026-1", nombre="2026-1",
            fecha_inicio=date(2026, 1, 1), fecha_fin=date(2026, 12, 31),
        )
        self.momento = MomentoAcademico.objects.create(
            periodo=periodo, nombre="Periodo completo",
            fecha_inicio=date(2026, 1, 1), fecha_fin=date(2026, 12, 31),
        )
        sede = Sede.objects.create(institucion=self.inst1, nombre="Sede principal")
        edificio = Edificio.objects.create(institucion=self.inst1, sede=sede, nombre="Edificio A")
        self.aula = Aula.objects.create(institucion=self.inst1, edificio=edificio, nombre="A-101", capacidad=30, tipo_espacio="AULA")
        self.aula_alterna = Aula.objects.create(institucion=self.inst1, edificio=edificio, nombre="A-102", capacidad=30, tipo_espacio="AULA")
        self.docente = Docente.objects.create(institucion=self.inst1, nombre="Ana Perez", identificacion="1", email="ana@example.com")
        self.clase = Clase.objects.create(
            institucion=self.inst1, docente=self.docente, aula=self.aula, periodo=periodo, momento=self.momento,
            asignatura="Matematicas", nrc="MAT-1", dia_semana=1,
            hora_inicio=time(8, 0), hora_fin=time(10, 0),
        )
        set_current_institucion(None)

    def test_unknown_tenant_cannot_read_tenant_data(self):
        self.assertEqual(Aula.objects.count(), 0)
        respuesta = self.client.get("/", HTTP_HOST="unknown.localhost")
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotContains(respuesta, "A-101")

    def test_agenda_contains_recurring_calendar_event(self):
        respuesta = self.client.get(f"/agenda-docente/{self.docente.id}/", HTTP_HOST="inst1.localhost")
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, '"daysOfWeek": [1]')
        self.assertContains(respuesta, "Matematicas")

    def test_reassignment_requires_post_and_uses_available_room(self):
        url = f"/conflictos/reasignar/{self.clase.id}/{self.aula_alterna.id}/"
        respuesta = self.client.get(url, HTTP_HOST="inst1.localhost")
        self.assertEqual(respuesta.status_code, 405)
        respuesta = self.client.post(url, HTTP_HOST="inst1.localhost")
        self.assertEqual(respuesta.status_code, 302)
        self.clase.refresh_from_db()
        self.assertEqual(self.clase.aula_id, self.aula_alterna.id)

    @override_settings(REQUIRE_LOGIN=True)
    def test_pilot_access_requires_an_account_from_the_current_institution(self):
        respuesta = self.client.get('/', HTTP_HOST='inst1.localhost')
        self.assertRedirects(respuesta, '/acceso/?next=/')

        user = get_user_model().objects.create_user(username='consulta', password='clave-segura')
        PerfilUsuario.objects.create(user=user, institucion=self.inst2, rol='CONSULTA')
        self.client.force_login(user)
        respuesta = self.client.get('/', HTTP_HOST='inst1.localhost')
        self.assertEqual(respuesta.status_code, 403)

        user.perfil_sigea.institucion = self.inst1
        user.perfil_sigea.save(update_fields=['institucion'])
        respuesta = self.client.get('/', HTTP_HOST='inst1.localhost')
        self.assertEqual(respuesta.status_code, 200)

    @override_settings(REQUIRE_LOGIN=True)
    def test_roles_protegen_carga_y_gestion_de_usuarios(self):
        consulta = get_user_model().objects.create_user(username='consulta-rol', password='ClaveSegura123!')
        PerfilUsuario.objects.create(user=consulta, institucion=self.inst1, rol='CONSULTA')
        self.client.force_login(consulta)

        respuesta = self.client.get('/usuarios/', HTTP_HOST='inst1.localhost')
        self.assertEqual(respuesta.status_code, 403)
        self.assertContains(
            respuesta,
            'Solo el administrador institucional puede gestionar usuarios.',
            status_code=403,
        )
        respuesta = self.client.post('/subir-excel/', HTTP_HOST='inst1.localhost')
        self.assertEqual(respuesta.status_code, 403)

        programador = get_user_model().objects.create_user(username='programador', password='ClaveSegura123!')
        PerfilUsuario.objects.create(user=programador, institucion=self.inst1, rol='PROGRAMADOR')
        self.client.force_login(programador)
        respuesta = self.client.post('/subir-excel/', HTTP_HOST='inst1.localhost')
        self.assertEqual(respuesta.status_code, 302)

    @override_settings(REQUIRE_LOGIN=True)
    def test_administrador_puede_crear_cuenta_de_su_institucion(self):
        admin = get_user_model().objects.create_user(username='admin-rol', password='ClaveSegura123!')
        PerfilUsuario.objects.create(user=admin, institucion=self.inst1, rol='ADMIN')
        self.client.force_login(admin)

        respuesta = self.client.post('/usuarios/', {
            'accion': 'crear',
            'username': 'piloto-consulta',
            'email': 'consulta@example.com',
            'rol': 'CONSULTA',
            'password': 'OtraClaveSegura123!',
        }, HTTP_HOST='inst1.localhost')
        self.assertRedirects(respuesta, '/usuarios/')
        perfil = PerfilUsuario.objects.get(user__username='piloto-consulta')
        self.assertEqual(perfil.institucion, self.inst1)
        self.assertEqual(perfil.rol, 'CONSULTA')

        respuesta = self.client.get('/usuarios/', HTTP_HOST='inst1.localhost')
        self.assertContains(respuesta, 'Programador académico')

    @override_settings(REQUIRE_LOGIN=True)
    def test_cierre_de_sesion_requiere_post_y_redirige_al_acceso(self):
        user = get_user_model().objects.create_user(username='cerrar-sesion', password='ClaveSegura123!')
        PerfilUsuario.objects.create(user=user, institucion=self.inst1, rol='CONSULTA')
        self.client.force_login(user)

        respuesta = self.client.post('/salir/', HTTP_HOST='inst1.localhost')
        self.assertRedirects(respuesta, '/acceso/')

    @override_settings(REQUIRE_LOGIN=True)
    def test_tablero_muestra_herramientas_segun_el_rol(self):
        consulta = get_user_model().objects.create_user(username='vista-consulta', password='ClaveSegura123!')
        PerfilUsuario.objects.create(user=consulta, institucion=self.inst1, rol='CONSULTA')
        self.client.force_login(consulta)
        respuesta = self.client.get('/', HTTP_HOST='inst1.localhost')
        self.assertContains(respuesta, 'Modo consulta')
        self.assertNotContains(respuesta, 'Importar Excel')
        self.assertNotContains(respuesta, 'Gestión de Usuarios')

        programador = get_user_model().objects.create_user(username='vista-programador', password='ClaveSegura123!')
        PerfilUsuario.objects.create(user=programador, institucion=self.inst1, rol='PROGRAMADOR')
        self.client.force_login(programador)
        respuesta = self.client.get('/', HTTP_HOST='inst1.localhost')
        self.assertContains(respuesta, 'Importar Excel')
        self.assertNotContains(respuesta, 'Gestión de Usuarios')

        admin = get_user_model().objects.create_user(username='vista-admin', password='ClaveSegura123!')
        PerfilUsuario.objects.create(user=admin, institucion=self.inst1, rol='ADMIN')
        self.client.force_login(admin)
        respuesta = self.client.get('/', HTTP_HOST='inst1.localhost')
        self.assertContains(respuesta, 'Gestión de Usuarios')


class BootstrapPilotCommandTests(TestCase):
    @patch.dict(os.environ, {
        'DEFAULT_TENANT_SUBDOMAIN': 'piloto-prueba',
        'INITIAL_ADMIN_USERNAME': 'admin-piloto',
        'INITIAL_ADMIN_PASSWORD': 'ClaveSegura123!',
        'INITIAL_ADMIN_EMAIL': 'admin@example.com',
    }, clear=False)
    def test_crea_institucion_y_administrador_de_forma_idempotente(self):
        call_command('bootstrap_pilot')
        call_command('bootstrap_pilot')

        institucion = Institucion.objects.get(subdominio='piloto-prueba')
        usuario = get_user_model().objects.get(username='admin-piloto')
        self.assertTrue(usuario.is_superuser)
        self.assertTrue(usuario.check_password('ClaveSegura123!'))
        self.assertEqual(usuario.perfil_sigea.institucion, institucion)
        self.assertEqual(usuario.perfil_sigea.rol, 'ADMIN')


class ExcelImporterTests(TestCase):
    def setUp(self):
        self.institucion = Institucion.objects.create(
            nombre='Institucion de prueba', subdominio='importacion',
            hora_inicio_jornada=time(6, 0), hora_fin_jornada=time(22, 0),
        )

    def crear_archivo(self, hora_inicio='0800'):
        libro = Workbook()
        hoja = libro.active
        hoja.append([
            'PERIODO', 'NRC', 'TITULO', 'NOMBRE_DOCENTE', 'SEDE', 'EDIFICIO',
            'SALON', 'HI', 'HF', 'L', 'M', 'I', 'J', 'V', 'S', 'D',
        ])
        hoja.append([
            '202610', 'NRC-1', 'Matematicas', 'Ana Perez', 'Sede piloto',
            'Edificio A', 'A-101', hora_inicio, '1000', 'X', '', '', '', '', '', '',
        ])
        from io import BytesIO
        contenido = BytesIO()
        libro.save(contenido)
        return SimpleUploadedFile(
            'programacion.xlsx',
            contenido.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    def test_crea_espacios_faltantes_y_conserva_horario_si_hay_errores(self):
        resultado = ExcelImporter(self.crear_archivo(), self.institucion).importar()
        self.assertEqual(resultado['errores'], [])
        self.assertEqual(resultado['total'], 1)
        aula = Aula.unfiltered.get(institucion=self.institucion, nombre='A-101')
        self.assertEqual(aula.capacidad, 30)

        resultado_invalido = ExcelImporter(
            self.crear_archivo(hora_inicio='hora-invalida'), self.institucion
        ).importar()
        self.assertTrue(resultado_invalido['errores'])
        self.assertEqual(Clase.unfiltered.filter(institucion=self.institucion).count(), 1)
