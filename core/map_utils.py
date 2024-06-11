from core.models import Carona, Combinado
from decouple import config
from geopy.geocoders import Nominatim


def obter_coordenadas_endereco(endereco):
    geolocator = Nominatim(user_agent="my_geocoder")

    location = geolocator.geocode(endereco)

    print(location)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        print(latitude, longitude)
        return latitude, longitude
    else:
        return None


def create_mapa_caminho(carona: Carona, combinado: Combinado):
    saida = combinado.deslocamento.ponto_saida_endereco

    pontos_encontro = carona.combinados.filter(
        deslocamento=combinado.deslocamento,
    )

    pontos_encontro = [
        ponto.endereco_ponto_encontro for ponto in pontos_encontro
    ]

    destino = combinado.deslocamento.ponto_destino_endereco

    pontos_passagem = [saida]

    pontos_passagem.extend(pontos_encontro)

    pontos_passagem.append(destino)

    return pontos_passagem
