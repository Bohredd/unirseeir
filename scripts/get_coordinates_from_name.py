from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_geocoder")

nome_local = "Centro de Tecnologia (CT), Santa Maria, RS, Brasil"

location = geolocator.geocode(nome_local)

if location:
    latitude = location.latitude
    longitude = location.longitude
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Local não encontrado.")

def get_coordinates_from_name(name, Endereco):

    geolocator = Nominatim(user_agent="my_geocoder")

    nome = f'{name} '