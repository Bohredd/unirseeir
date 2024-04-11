# 1 * Rodar makemigrations
import subprocess

resultado = subprocess.run(
    "python manage.py makemigrations",
    shell=True,
    capture_output=True,
    text=True,
)

# 2 * Rodar mirate
print(resultado.returncode)

if resultado.returncode == 0:
    resultado = subprocess.run(
        "python manage.py migrate",
        shell=True,
        capture_output=True,
        text=True,
    )
    print("migrate rodado")

# 3 * Carregar dados

print(resultado.returncode)

if resultado.returncode == 0:

    instalacao_fixtures = subprocess.run(
        "python manage.py loaddata dump.yaml",
    )

    print(instalacao_fixtures)

    if instalacao_fixtures.returncode == 0:
        print("Banco configurado, migrations executadas e dados intalados.")
