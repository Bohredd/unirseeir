import subprocess

# Comando para mudar para o diretório pai
cd_comando = "cd .."

# Comando para rodar makemigrations
makemigrations_comando = "python manage.py makemigrations"

# Comando para rodar migrate
migrate_comando = "python manage.py migrate"

# Comando para carregar dados
loaddata_comando = "python manage.py loaddata dump.yaml"

# Executar o comando cd ..
subprocess.run(cd_comando, shell=True)

# Executar o comando makemigrations
resultado_makemigrations = subprocess.run(makemigrations_comando, shell=True, capture_output=True, text=True)

# Executar o comando migrate se makemigrations for bem-sucedido
if resultado_makemigrations.returncode == 0:
    resultado_migrate = subprocess.run(migrate_comando, shell=True, capture_output=True, text=True)
    print("migrate rodado")

    # Executar o comando loaddata se migrate for bem-sucedido
    if resultado_migrate.returncode == 0:
        resultado_loaddata = subprocess.run(loaddata_comando, shell=True, capture_output=True, text=True)
        print(resultado_loaddata)

        if resultado_loaddata.returncode == 0:
            print("Banco configurado, migrations executadas e dados instalados.")
