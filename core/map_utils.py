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

    print(saida)

    destino = combinado.deslocamento.ponto_destino_endereco

    print(destino)

    coordenadas = []

    for ponto in carona.combinados.all():
        print(ponto.endereco_ponto_encontro)
        coordenadas.append(obter_coordenadas_endereco(ponto.endereco_ponto_encontro))

    url = f"""
    https://api.tomtom.com/routing/1/calculateRoute/52.50931,13.42936:52.50274,13.43872/json?key={config("TOMTOM_ACCESS_KEY")}"""
