# coding: utf-8
from django.db import models


class GeoCoding(models.Model):
    lat = models.DecimalField(
        max_digits=16,
        decimal_places=14,
        default=55.0322127,
        verbose_name='широта откуда'
    )
    lon = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        default=75.6545329,
        verbose_name='долгота откуда'
    )
    place_id = models.CharField(
        max_length=225,
        verbose_name='идентификатор города'
    )

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'геокодинг'
        verbose_name_plural = 'геокодинг'


class TransGeoData(models.Model):
    street_number = models.CharField(
        max_length=80,
        verbose_name='номер улицы'
    )
    street_title = models.CharField(
        max_length=120,
        verbose_name='название улицы'
    )
    political_town = models.CharField(
        max_length=120,
        verbose_name='название города'
    )
    political_area = models.CharField(
        max_length=255,
        verbose_name='название области'
    )
    country = models.CharField(
        max_length=80,
        verbose_name='название страны'
    )
    postal_code = models.PositiveIntegerField(
        default=0,
        verbose_name='индекс'
    )
    geocoding = models.ForeignKey(
        GeoCoding,
        blank=True, null=True,
        related_name='lang_address_geocode',
        verbose_name='гео данные'
    )

    def __unicode__(self):
        return u'(%s) %s' % (self.political_town, self.street_title,)

    class Meta:
        verbose_name = 'перевод адреса'
        verbose_name_plural = 'переводы адресов'
