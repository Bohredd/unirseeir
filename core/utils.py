import datetime
import re
import requests
import PyPDF2
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unirseir.settings")
import django

django.setup()
from core.models import Carona


def generate_pdf(carona: Carona):

    hoje = datetime.datetime.now().date().strftime("%d de %B de %Y")

    print("hoje é ", hoje)

    env = Environment(loader=FileSystemLoader("data/templates"))
    template = env.get_template("contrato.html")
    rendered_html = template.render(carona=carona, hoje_str=hoje)

    output_pdf = "output.pdf"
    HTML(string=rendered_html).write_pdf(output_pdf)


def verificar_matricula_valida(comprovante, matricula):

    arquivo = PyPDF2.PdfReader(comprovante)
    pagina = arquivo.pages[0]
    texto = pagina.extract_text()

    if matricula in texto:

        ano_atual = datetime.datetime.now().date().strftime("%Y")
        regex_ano_atual_semestre = r'Período: (\d{4}) - (\d{1})'
        match = re.search(regex_ano_atual_semestre, texto)

        if match:
            ano_matricula = match.group(1)
            semestre_matricula = match.group(2)

            if str(ano_matricula) == ano_atual:

                regex_codigo_cadeira = r"\b[A-Za-z]{3}\d{4}\b"

                cadeiras_matriculadas = re.findall(regex_codigo_cadeira, texto)

                if len(cadeiras_matriculadas) > 0:

                    regex_codigo_autenticacao_hash = r"Autenticação: (\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4})"

                    resultado = re.search(regex_codigo_autenticacao_hash, texto)

                    if resultado:
                        codigo_autenticacao_hash = resultado.group(1)

                        url_download_arquivo = f"https://www.ufsm.br/autenticacao/index.html?hash={codigo_autenticacao_hash}"

                        response = requests.get(url_download_arquivo)

                        if response.status_code == 200 and 'Content-Disposition' in response.headers:
                            return True
    return False


print(verificar_matricula_valida(
    "/home/dev/Downloads/Comprovante de Matrcula.pdf", "202220628"
))

# generate_pdf(Carona.objects.first())
