# Generated by Django 4.2.11 on 2024-04-03 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_caroneiro_user_motorista_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='carona',
            name='ativa',
            field=models.BooleanField(default=True),
        ),
    ]