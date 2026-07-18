from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0004_importacionprogramacion'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='clase',
            index=models.Index(
                fields=['institucion', 'aula', 'dia_semana', 'hora_inicio', 'hora_fin'],
                name='clase_ins_aula_horario_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='clase',
            index=models.Index(
                fields=['institucion', 'docente', 'dia_semana'],
                name='clase_ins_docente_dia_idx',
            ),
        ),
    ]
