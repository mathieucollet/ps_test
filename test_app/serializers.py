import requests
from rest_framework import serializers

from test_app.models import Region, County, City


def get_nominatim(state: str, field: str) -> str:
    """ Get nominatim information for a specific state

    :param state: string The name of the state
    :param field: The field to return in the response
    :return: string """

    url = "https://nominatim.openstreetmap.org/search"
    params = {'country': 'France', 'state': state, 'format': 'json'}
    response = requests.get(url, params)
    json = response.json()

    data = json[0][field] if json else 'Nominatim n\'a pas trouvé de correspondance'

    return data


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    # Annotation fields
    totalPopulation = serializers.DecimalField(max_digits=10, decimal_places=1, coerce_to_string=False)
    totalArea = serializers.IntegerField()
    # Method fields
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()

    @staticmethod
    def get_lat(obj):
        return get_nominatim(obj.name, 'lat')

    @staticmethod
    def get_lon(obj):
        return get_nominatim(obj.name, 'lon')

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
