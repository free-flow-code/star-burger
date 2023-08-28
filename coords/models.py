import requests
from django.db import models
from django.utils import timezone
from django.conf import settings
from .yandex_geo_funcs import fetch_coordinates


class PlaceQuerySet(models.QuerySet):

    def get_coordinates(self, address):
        place, created = self.get_or_create(
            address=address
            )

        try:
            if created or not place.created_at:
                place.lon, place.lat = fetch_coordinates(settings.YANDEX_API_KEY, address)
                place.created_at = timezone.now()
                place.save()
                return place.lon, place.lat
        except requests.exceptions.RequestException as err:
            print(err)

        return place.lon, place.lat


class Place(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=300,
        unique=True
    )
    lon = models.FloatField(
        'Долгота',
        null=True,
    )
    lat = models.FloatField(
        'Широта',
        null=True
    )
    created_at = models.DateTimeField(
        'Дата создания',
        null=True
    )

    objects = PlaceQuerySet.as_manager()

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return f'{self.address}: {self.created_at}'