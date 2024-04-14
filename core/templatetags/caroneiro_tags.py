from django import template
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

register = template.Library()

@register.simple_tag
def get_lat_long_from_cep(cep):
    geolocator = Nominatim(user_agent="myGeocoder")
    print(cep)
    location = geolocator.geocode({"postalcode": cep}, exactly_one=True)
    if location:
        return location.latitude, location.longitude
    return None, None


@register.simple_tag
def get_menor_distancia_cep(latitude, longitude, cep):
    print(latitude, longitude)
    print(cep)
    cep_latitude, cep_longitude = get_lat_long_from_cep(cep)
    if cep_latitude is None or cep_longitude is None:
        return None

    distancia = geodesic((latitude, longitude), (cep_latitude, cep_longitude)).meters
    return (
        float(distancia)
        if distancia is not None
        else "Não foi possível obter dados geográficos."
    )
