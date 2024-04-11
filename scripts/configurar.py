# 1 * Rodar makemigrations
import subprocess
resultado = subprocess.run(
    "python manage.py makemigrations",
    shell=True,
    capture_output=True,
    text=True,
)

# 2 * Rodar mirate
if resultado.returncode == 0:
    resultado = subprocess.run(
        "python manage.py migrate",
        shell=True,
        capture_output=True,
        text=True,
    )

# 3 * Carregar dados

if resultado.returncode == 0:
    instalacao_fixtures = subprocess.run(
        "python manage.py loaddata dump.yaml",
        shell=True,
        capture_output=True,
        text=True,
    )
    if instalacao_fixtures.returncode == 0:
        print("Banco configurado, migrations executadas e dados intalados.")
