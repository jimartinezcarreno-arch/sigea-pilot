# Normaliza las etiquetas visibles de los roles; los valores almacenados no cambian.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0002_perfilusuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='rol',
            field=models.CharField(
                choices=[
                    ('ADMIN', 'Administrador institucional'),
                    ('PROGRAMADOR', 'Programador académico'),
                    ('CONSULTA', 'Consulta'),
                ],
                default='CONSULTA',
                max_length=20,
            ),
        ),
    ]
