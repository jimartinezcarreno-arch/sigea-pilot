# Generated manually for import history and rollback support.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0003_alter_perfilusuario_rol'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportacionProgramacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo_nombre', models.CharField(max_length=255)),
                ('tipo', models.CharField(
                    choices=[
                        ('IMPORTACION', 'Importación de Excel'),
                        ('RESTAURACION', 'Restauración de historial'),
                    ],
                    default='IMPORTACION',
                    max_length=20,
                )),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('total_clases', models.PositiveIntegerField(default=0)),
                ('respaldo_anterior', models.JSONField(blank=True, default=list)),
                ('creado_por', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='importaciones_sigea',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.institucion')),
            ],
            options={'ordering': ['-fecha_creacion']},
        ),
    ]
