# Generated by Django 4.2.11 on 2024-04-11 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_rename_hora_ida_deslocamento_horario_saida_ponto_saida_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deslocamento',
            name='ponto_destino_endereco',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deslocamento',
            name='ponto_saida_endereco',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
    ]
