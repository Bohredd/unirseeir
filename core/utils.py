import base64
import io
import os
import re
import requests
import PyPDF2
import json
from django.contrib.auth.hashers import check_password
from geopy.exc import GeocoderUnavailable
from xhtml2pdf import pisa
from django.http import HttpResponse
from config.models import Config, CoordenadaCEP
from core.contrato import get_template_contrato
from django.contrib.auth.models import User
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import random
import string
from PIL import Image
import math


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
        regex_ano_atual_semestre = r"Período: (\d{4}) - (\d{1})"
        match = re.search(regex_ano_atual_semestre, texto)

        if match:
            ano_matricula = match.group(1)
            semestre_matricula = match.group(2)

            config = Config.objects.first()

            if config is not None:
                if (
                    int(ano_matricula) == config.ano
                    and int(semestre_matricula) == config.semestre
                ):
                    regex_codigo_cadeira = r"\b[A-Za-z]{3}\d{4}\b"

                    cadeiras_matriculadas = re.findall(regex_codigo_cadeira, texto)

                    if len(cadeiras_matriculadas) > 0:
                        regex_codigo_autenticacao_hash = r"Autenticação: (\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4}\.\w{4})"

                        resultado = re.search(regex_codigo_autenticacao_hash, texto)

                        if resultado:
                            codigo_autenticacao_hash = resultado.group(1)

                            url_download_arquivo = f"https://www.ufsm.br/autenticacao/index.html?hash={codigo_autenticacao_hash}"

                            response = requests.get(url_download_arquivo)

                            if (
                                response.status_code == 200
                                and "Content-Disposition" in response.headers
                            ):
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
        nome_remetente, chave_remetente, str(float(custo) * 1.05), cidade, razao
    )
    qrcode = qr.gerarPayload()

    return qrcode


def get_user(cleaned_data):

    matricula = cleaned_data["matricula"]
    senha = cleaned_data["senha"]
    tipo = cleaned_data["tipo"]

    return User.objects.filter(
        username=matricula,
    ).first()


def get_message_login(cleaned_data):

    matricula = cleaned_data["matricula"]
    senha = cleaned_data["senha"]

    if User.objects.filter(username=matricula).exists():

        user = User.objects.get(username=matricula)

        if check_password(senha, user.password):
            # if
            return "Matrícula inválida, tente novamente"

        else:
            return "Senha inválida, tente novamente"
    elif not User.objects.filter(username=matricula).exists():
        return "Usuário inexistente, caso deseja, crie uma conta!"

    return None


def get_menor_distancia_deslocamentos(latitude, longitude, carona):
    geolocator = Nominatim(user_agent="my_geocoder")

    deslocamentos = carona.motorista.deslocamentos.all()
    coord1 = (latitude, longitude)
    coord2 = None
    menor_distancia = None
    for deslocamento in deslocamentos:

        if deslocamento.ponto_saida:
            coord2 = (deslocamento.ponto_saida.x, deslocamento.ponto_saida.y)
        else:
            localizacao = geolocator.geocode(deslocamento.ponto_saida_endereco)
            if localizacao:
                latitude_endereco = localizacao.latitude
                longitude_endereco = localizacao.longitude

                coord2 = (latitude_endereco, longitude_endereco)

        if menor_distancia is None:
            menor_distancia = geodesic(coord1, coord2).meters
            print(menor_distancia, "era none")
        else:
            if menor_distancia < geodesic(coord1, coord2).meters:
                print(
                    geodesic(coord1, coord2).meters,
                    " essa é menor que a antiga ",
                    menor_distancia,
                )
                menor_distancia = geodesic(coord1, coord2).meters

    if not deslocamentos:
        coord2 = get_coordinates_from_cep(carona.motorista.endereco.cep)
        print("PELO CEP!", coord2)
        menor_distancia = geodesic(coord1, coord2).meters

    print("Menor distancia: ", menor_distancia)
    return (
        f"{menor_distancia:.1f}"
        if menor_distancia is not None
        else "Não foi possível obter dados geográficos."
    )


def get_lat_long_from_cep(cep, request):

    coordenadaCEP = CoordenadaCEP.objects.filter(cep=cep, usuario=request.user)
    if coordenadaCEP.exists():
        coordenadaCEP = coordenadaCEP.first()
        return coordenadaCEP.latitude, coordenadaCEP.longitude
    else:
        try:
            geolocator = Nominatim(user_agent="myGeocoder")
            location = geolocator.geocode({"postalcode": cep}, exactly_one=True)
            if location:
                print(
                    location, " location ", location.latitude, " location ", location.longitude
                )
                CoordenadaCEP.objects.create(
                    usuario=request.user,
                    cep=cep,
                    latitude=location.latitude,
                    longitude=location.longitude,
                )
                return location.latitude, location.longitude
        except Exception as e:
            return None, None
    return None, None


def get_menor_distancia_cep(latitude, longitude, cep, request):
    cep_latitude, cep_longitude = get_lat_long_from_cep(cep, request)
    if cep_latitude is None or cep_longitude is None:
        return None
    print("request: ", request)
    distancia = geodesic((latitude, longitude), (cep_latitude, cep_longitude)).meters
    print("Distancia: ", distancia, " metros")
    return (
        float(distancia)
        if distancia is not None
        else "Não foi possível obter dados geográficos."
    )


def get_address_by_cep(cep):
    address = requests.get("https://viacep.com.br/ws/{}/json/".format(cep))
    if address.status_code == 200:
        data = json.loads(address.content)
        return data

    return None


def get_coordinates_from_cep(cep):
    url = f"https://nominatim.openstreetmap.org/search?q={cep},br&format=json"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
    else:
        return None


def gerar_senha(tamanho=16):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = "".join(random.choice(caracteres) for _ in range(tamanho))
    return senha


def combinar_imagens(membros, largura_quadro=300, altura_quadro=300):
    lista_imagens = []

    for membro in membros:
        lista_imagens.append(
            os.path.abspath(os.path.join(os.getcwd(), membro.foto.url[1:]))
        )

    num_imagens = len(lista_imagens)
    colunas = int(math.ceil(math.sqrt(num_imagens)))
    linhas = int(math.ceil(num_imagens / colunas))
    largura_nova_imagem = colunas * largura_quadro
    altura_nova_imagem = linhas * altura_quadro

    nova_imagem = Image.new("RGB", (largura_nova_imagem, altura_nova_imagem))

    for i, imagem_path in enumerate(lista_imagens):
        imagem = Image.open(imagem_path)
        imagem_redimensionada = imagem.resize((largura_quadro, altura_quadro))
        coluna = i % colunas
        linha = i // colunas
        nova_imagem.paste(
            imagem_redimensionada, (coluna * largura_quadro, linha * altura_quadro)
        )
        imagem.close()

    buffer = io.BytesIO()

    nova_imagem.save(buffer, "JPEG")

    imagem_data = buffer.getvalue()

    return f"data:image/jpeg;base64,{base64.b64encode(imagem_data).decode()}"
