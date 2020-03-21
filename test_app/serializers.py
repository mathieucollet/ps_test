import requests
from rest_framework import serializers

from test_app.models import Region, County, City

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def get_nominatim(obj):
    params = {'country': 'France', 'state': obj.name, 'format': 'json'}
    response = requests.get(NOMINATIM_URL, params)
    data = response.json()
    return data


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    totalPopulation = serializers.DecimalField(max_digits=10, decimal_places=1, coerce_to_string=False)
    totalArea = serializers.IntegerField()
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()

    @staticmethod
    def get_lat(obj):
        data = get_nominatim(obj)
        return data[0]['lat'] if data else 'Nominatim n\'a pas trouvé de correspondance'

    @staticmethod
    def get_lon(obj):
        data = get_nominatim(obj)
        return data[0]['lon'] if data else 'Nominatim n\'a pas trouvé de correspondance'

    class Meta:
        model = Region
        fields = ['code', 'name', 'totalPopulation', 'totalArea', 'lat', 'lon']


class CountySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = County
        fields = ['code', 'name']


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ['code_insee', 'code_postal', 'name', 'population', 'area']
