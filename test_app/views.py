from django.db.models import Sum
from rest_framework import viewsets

from test_app.models import Region
from test_app.serializers import RegionSerializer


class RegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows regions to be viewed
    """
    queryset = Region.objects.annotate(
        totalPopulation=Sum('counties__cities__population'),
        totalArea=Sum('counties__cities__area'),
    ).order_by('code')

    serializer_class = RegionSerializer
