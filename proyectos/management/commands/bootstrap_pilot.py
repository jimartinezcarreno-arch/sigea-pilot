import os
from datetime import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from proyectos.models import Institucion, PerfilUsuario


class Command(BaseCommand):
    help = 'Prepara de forma idempotente la instituci\u00f3n y cuenta iniciales del piloto.'

    def handle(self, *args, **options):
        subdominio = os.environ.get('DEFAULT_TENANT_SUBDOMAIN', 'sigea')
        nombre_institucion = os.environ.get('PILOT_INSTITUTION_NAME', 'SIGEA Pilot')

        institucion, creada = Institucion.objects.get_or_create(
            subdominio=subdominio,
            defaults={
                'nombre': nombre_institucion,
                'hora_inicio_jornada': time(6, 0),
                'hora_fin_jornada': time(22, 0),
                'activo': True,
            },
        )
        if not institucion.activo:
            institucion.activo = True
            institucion.save(update_fields=['activo'])

        estado_institucion = 'creada' if creada else 'verificada'
        self.stdout.write(self.style.SUCCESS(
            f'Instituci\u00f3n piloto {estado_institucion}: {institucion.nombre} ({subdominio}).'
        ))

        username = os.environ.get('INITIAL_ADMIN_USERNAME')
        password = os.environ.get('INITIAL_ADMIN_PASSWORD')
        email = os.environ.get('INITIAL_ADMIN_EMAIL', '')

        if not username or not password:
            self.stdout.write(
                'Cuenta inicial no creada: define INITIAL_ADMIN_USERNAME e '
                'INITIAL_ADMIN_PASSWORD como secretos del entorno para habilitarla.'
            )
            return

        User = get_user_model()
        usuario, creado = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        if creado:
            usuario.set_password(password)
            usuario.save()
        elif not usuario.check_password(password):
            self.stdout.write(self.style.WARNING(
                f'La cuenta {username!r} ya existe; se conserva su contrase\u00f1a actual.'
            ))

        PerfilUsuario.objects.update_or_create(
            user=usuario,
            defaults={
                'institucion': institucion,
                'rol': 'ADMIN',
                'activo': True,
            },
        )
        estado_usuario = 'creada' if creado else 'verificada'
        self.stdout.write(self.style.SUCCESS(
            f'Cuenta administradora {estado_usuario}: {username!r}.'
        ))
