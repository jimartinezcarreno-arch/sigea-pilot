# Generated manually for the pilot access profile.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('ADMIN', 'Administrador institucional'), ('PROGRAMADOR', 'Programador acadÃ©mico'), ('CONSULTA', 'Consulta')], default='CONSULTA', max_length=20)),
                ('activo', models.BooleanField(default=True)),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='proyectos.institucion')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_sigea', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
