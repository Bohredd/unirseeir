import re
import requests


def get_coordinates_via_address(*args, **kwargs):

    url_base = "https://www.google.com/maps/search/"

    url = "https://www.google.com/maps/search/rua+clenio+luiz+denardin,+432,+boi+morto,+santa+maria,+rio+grande+do+sul"

    response = requests.get(url, allow_redirects=False)
    # PADRAO:
    # Avenida+Fernando+Ferrari
    # +-+Nossa+Senhora+de+Lourdes,+Santa+Maria+-+Rio+Grande+Do+Sul

    regex_coordenada = r"@(-?\d+\.\d+,-?\d+\.\d+)"

    coordenadas = re.findall(regex_coordenada, str(response.content))

    if coordenadas:
        coordenadas = coordenadas[0]
        print(coordenadas)
    else:
        coordenadas = None


get_coordinates_via_address()
