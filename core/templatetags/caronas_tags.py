from django import template
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

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

    print("Menor distancia: ", menor_distancia)
    return float(menor_distancia)
