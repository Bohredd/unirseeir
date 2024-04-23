import datetime
import locale
from django import template
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import folium
from geopy.exc import GeocoderUnavailable
from django.utils import timezone
from core.utils import get_coordinates_from_cep

register = template.Library()


@register.simple_tag
def get_distancia_saida(latitude, longitude, carona):
    print(latitude, longitude, carona)
    print("testeee")

    geolocator = Nominatim(user_agent="my_geocoder")

    deslocamentos = carona.motorista.deslocamentos.all()
    coord1 = (latitude, longitude)
    coord2 = None
    menor_distancia = None
    for deslocamento in deslocamentos:

        if deslocamento.ponto_saida:
            coord2 = (deslocamento.ponto_saida.x, deslocamento.ponto_saida.y)
            print(coord2, "tem ponto_saida")
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
        float(menor_distancia)
        if menor_distancia is not None
        else "Não foi possível obter dados geográficos."
    )


def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_app")
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except GeocoderUnavailable:
        return None


@register.simple_tag
def gerar_mapa(deslocamento):
    endereco_saida = deslocamento.ponto_saida_endereco
    endereco_destino = deslocamento.ponto_destino_endereco

    coordenadas_saida = get_coordinates(endereco_saida)
    coordenadas_destino = get_coordinates(endereco_destino)

    if coordenadas_saida and coordenadas_destino:
        mapa = folium.Map(
            location=[coordenadas_saida[0], coordenadas_saida[1]], zoom_start=15
        )

        folium.Marker(
            [coordenadas_saida[0], coordenadas_saida[1]], popup="Ponto de Saída"
        ).add_to(mapa)
        folium.Marker(
            [coordenadas_destino[0], coordenadas_destino[1]], popup="Ponto de Destino"
        ).add_to(mapa)

        folium.PolyLine(
            locations=[
                (coordenadas_saida[0], coordenadas_saida[1]),
                (coordenadas_destino[0], coordenadas_destino[1]),
            ],
            color="blue",
        ).add_to(mapa)

        mapa_html = mapa._repr_html_()

        return mapa_html
    else:
        return "Não foi possível obter as coordenadas para o deslocamento."


@register.simple_tag
def get_proximo_compromisso(carona, user):
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

    hoje = datetime.datetime.now().date()
    dia_semana_hoje = hoje.strftime("%A")

    print(hoje)
    print(dia_semana_hoje)

    proximo_compromisso = (
        carona.combinados.all()
        .filter(
            deslocamento__dia_semana=dia_semana_hoje,
            deslocamento__horario_saida_ponto_saida__gte=timezone.now(),
        )
        .order_by("deslocamento__dia_semana", "horario_encontro_ponto_encontro")
        .first()
    )

    print(proximo_compromisso)

    if proximo_compromisso:
        return proximo_compromisso

    proximo_compromisso = (
        carona.combinados.all()
        .order_by("deslocamento__dia_semana", "horario_encontro_ponto_encontro")
        .first()
    )

    print(proximo_compromisso)

    return proximo_compromisso
