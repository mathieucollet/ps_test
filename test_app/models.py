# Create your models here.
from django.db import models


class Region(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=100)


class County(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='counties', on_delete=models.CASCADE)


class City(models.Model):
    code_insee = models.CharField(max_length=10)
    code_postal = models.IntegerField()
    name = models.CharField(max_length=100)
    population = models.DecimalField(max_digits=5, decimal_places=2)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    county = models.ForeignKey(County, related_name='cities', on_delete=models.CASCADE)
