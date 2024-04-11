import subprocess
import sys
import venv
from pathlib import Path

if sys.version_info < (3, 3):
    print("Este script requer Python 3.3 ou superior.")
    sys.exit(1)

venv_dir = "/comp/venv"

venv.create(venv_dir, with_pip=True)

pip_path = Path(venv_dir) / "Scripts" / "pip" if sys.platform == "win32" else Path(venv_dir) / "bin" / "pip"

subprocess.run([pip_path, "install", "-r", "requirements.txt"])

print("Ambiente virtual criado e pacotes instalados com sucesso!")
