# Generated by Django 4.2.11 on 2024-04-04 23:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_remove_motorista_ponto_saida_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem', models.TextField()),
                ('enviado_por_tipo', models.CharField(choices=[('caroneiro', 'Caroneiro'), ('motorista', 'Motorista')], max_length=100)),
                ('enviado_para_tipo', models.CharField(choices=[('caroneiro', 'Caroneiro'), ('motorista', 'Motorista')], max_length=100)),
                ('carona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carona')),
                ('enviado_para', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enviado_para', to=settings.AUTH_USER_MODEL)),
                ('enviado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enviado_por', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
