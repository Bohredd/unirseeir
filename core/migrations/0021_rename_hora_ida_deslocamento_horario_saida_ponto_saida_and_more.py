# Generated by Django 4.2.11 on 2024-04-11 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_deslocamento_dia_semana'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deslocamento',
            old_name='hora_ida',
            new_name='horario_saida_ponto_saida',
        ),
        migrations.RemoveField(
            model_name='combinado',
            name='ida',
        ),
        migrations.RemoveField(
            model_name='combinado',
            name='volta',
        ),
        migrations.RemoveField(
            model_name='deslocamento',
            name='hora_volta',
        ),
    ]
