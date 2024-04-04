import io
import re
import requests
import PyPDF2
from xhtml2pdf import pisa
from django.http import HttpResponse
from config.models import Config
from core.data.templates.contrato import get_template_contrato


def generate_pdf(carona, caroneiro, tipo):

    template_contrato = get_template_contrato(carona, caroneiro, tipo)
    pdf_file = io.BytesIO()
    pisa.CreatePDF(template_contrato, dest=pdf_file)

    response = HttpResponse(pdf_file.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="contrato.pdf"'

    return response


def verificar_matricula_valida(comprovante, aluno):

    arquivo = PyPDF2.PdfReader(comprovante)
    pagina = arquivo.pages[0]
    texto = pagina.extract_text()

    if aluno.matricula in texto and aluno.nome.upper() in texto:
        print("nome")
        regex_ano_atual_semestre = r"Período: (\d{4}) - (\d{1})"
        match = re.search(regex_ano_atual_semestre, texto)

        if match:
            print("match")
            ano_matricula = match.group(1)
            semestre_matricula = match.group(2)

            config = Config.objects.first()

            if config is not None:
                if (
                    int(ano_matricula) == config.ano
                    and int(semestre_matricula) == config.semestre
                ):
                    print("ano e semestre")
                    regex_codigo_cadeira = r"\b[A-Za-z]{3}\d{4}\b"

                    cadeiras_matriculadas = re.findall(regex_codigo_cadeira, texto)

                    if len(cadeiras_matriculadas) > 0:
                        print("tem cadeiras")
                        regex_codigo_autenticacao_hash = r"Autenticação: (\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4})"

                        resultado = re.search(regex_codigo_autenticacao_hash, texto)

                        if resultado:
                            print("tem hash")
                            codigo_autenticacao_hash = resultado.group(1)

                            url_download_arquivo = f"https://www.ufsm.br/autenticacao/index.html?hash={codigo_autenticacao_hash}"

                            response = requests.get(url_download_arquivo)

                            if (
                                response.status_code == 200
                                and "Content-Disposition" in response.headers
                            ):
                                print("hash valido")
                                return True
    return False


def obter_qr_code_pix(
    nome_remetente,
    chave_remetente,
    custo,
    cidade="Santa Maria, RS",
    razao="Ajuda de Custos UNIr-se e Ir",
):

    from core.pix import GerarPix

    qr = GerarPix(
        nome_remetente, chave_remetente, str(float(custo) * 1.1), cidade, razao
    )
    qrcode = qr.gerarPayload()

    return qrcode