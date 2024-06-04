from django import template
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

from config.models import CoordenadaCEP

register = template.Library()


@register.simple_tag
def get_lat_long_from_cep(cep, request):
    coordenadaCEP = CoordenadaCEP.objects.filter(cep=cep, usuario=request.user)

    if coordenadaCEP.exists():
        coordenadaCEP = coordenadaCEP.first()
        return coordenadaCEP.latitude, coordenadaCEP.longitude
    else:
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.geocode({"postalcode": cep}, exactly_one=True)
        print(
            location, " location ", location.latitude, " location ", location.longitude
        )
        if location:
            CoordenadaCEP.objects.create(
                usuario=request.user,
                cep=cep,
                latitude=location.latitude,
                longitude=location.longitude,
            )
            return location.latitude, location.longitude


@register.simple_tag
def get_menor_distancia_cep(latitude, longitude, cep, request):
    print(latitude, longitude)
    print(cep)
    cep_latitude, cep_longitude = get_lat_long_from_cep(cep, request)
    if cep_latitude is None or cep_longitude is None:
        return None

    distancia = geodesic((latitude, longitude), (cep_latitude, cep_longitude)).meters
    return (
        float(distancia)
        if distancia is not None
        else "Não foi possível obter dados geográficos."
    )
