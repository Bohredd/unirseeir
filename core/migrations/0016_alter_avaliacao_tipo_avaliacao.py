# Generated by Django 4.2.11 on 2024-04-07 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_avaliacao_avaliado_solicitacao_resposta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliacao',
            name='tipo_avaliacao',
            field=models.CharField(choices=[('motorista', 'Motorista'), ('caroneiro', 'Caroneiro')], max_length=30, verbose_name='Quem foi avaliado é o que:'),
        ),
    ]
