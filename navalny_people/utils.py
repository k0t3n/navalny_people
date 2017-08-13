import json
import os
import uuid
from collections import namedtuple
from datetime import datetime

from django.conf import settings

from geodata.models import TransGeoData, GeoCoding


def upload_to(instance, filename):
    """
    Returns path to upload file as @string
    @string: app_name/model_name/4_uuid4_symbols/uuid4.ext
    """
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (str(uuid.uuid4()), ext)
    basedir = os.path.join(instance._meta.app_label,
                           instance.__class__.__name__.lower())
    return os.path.join(basedir, filename[:4], filename)


def decode_address_by_googlemaps(value):
    """
    :param value: string address for geocode to geo data
    :return: saved instance to model
    """
    import geocoder
    options_geocoder = {'key': settings.GOOGLEMAPS_KEY, 'language': 'ru'}
    gmaps_data = geocoder.google(value.replace(' ', '-'), **options_geocoder)
    if gmaps_data.json.get('status', None) == 'zero_results'.upper():
        value = value.replace(' ', '')
        value = value[value.index(',') + 1:]
        value = value[1:] if value[0] == ' ' else value
        gmaps_data = geocoder.google(value, **options_geocoder)
    qs_geocode = {'lat': gmaps_data.lat, 'lon': gmaps_data.lng}
    if (qs_geocode['lat'] or qs_geocode['lon']) is None:
        return None
    else:
        geo_code, created_geo = GeoCoding.objects. \
            get_or_create(defaults=qs_geocode, place_id=gmaps_data.place)
        qs_trans_geocode = {
            'street_number': gmaps_data.street_number
            if gmaps_data.street_number else '',
            'street_title': gmaps_data.street_long
            if gmaps_data.street_long else '',
            'political_town': gmaps_data.city_long
            if gmaps_data.city_long else '',
            'political_area': gmaps_data.province_long
            if gmaps_data.province_long else '',
            'country': gmaps_data.country_long
            if gmaps_data.country_long else '',
        }
        try:
            qs_trans_geocode.update({
                'postal_code': gmaps_data.postal
                if type(gmaps_data.postal) is int else 0
            })
        except (ValueError, TypeError):
            qs_trans_geocode.update({'postal_code': 0})
        trans_geo_data, created = TransGeoData.objects. \
            get_or_create(**qs_trans_geocode)
        trans_geo_data.geocoding = geo_code
        trans_geo_data.save()

        return geo_code


def decode_latlon_by_googlemaps(lat, lng, city=None):
    """
    :param lat: float value by latitude
    :param lng: float value by longitude
    :param city: forward return title of city
    :return: saved instance to model
    """
    import geocoder
    coords_list = [lat, lng]
    options_geocoder = {'key': settings.GOOGLEMAPS_KEY}
    gmaps_data = geocoder.reverse(coords_list, **options_geocoder)
    if gmaps_data.json.get('status', None) == 'zero_results'.upper():
        lat += .00001
        lng += .00001
        gmaps_data = geocoder.reverse(coords_list, **options_geocoder)
    if city is not None:
        return gmaps_data.city
    return gmaps_data.address


def GeoCodeResponse(pk, output_data, fields=[]):
    """
    :param lang: int value by language for translate response
    :param pk: primary key by instance model
    :param output_data: type output data in dict or string
    :param fields: list of fields for choose param values
    :return: response dict with geo data
    """
    geo = GeoCoding.objects.prefetch_related('lang_address_geocode'). \
        filter(**{'person_geodata': pk}). \
        values('lang_address_geocode__political_town',
               'lang_address_geocode__political_area',
               'lang_address_geocode__street_number',
               'lang_address_geocode__street_title',
               'lang_address_geocode__postal_code',
               'lang_address_geocode__country',
               'lat', 'lon'). \
        first()
    if geo is not None:
        if type(output_data) is dict:
            geo_data = {}
            for field in fields:
                if 'political_town' in field:
                    geo_data.update({'political_town':
                                    geo['lang_address_geocode__political_town']}
                                    )
                elif 'political_area' in field:
                    geo_data.update({'political_area':
                                    geo['lang_address_geocode__political_area']}
                                    )
                elif 'street_number' in field:
                    geo_data.update({'street_number':
                                    geo['lang_address_geocode__street_number']}
                                    )
                elif 'street_title' in field:
                    geo_data.update({'street_title':
                                    geo['lang_address_geocode__street_title']}
                                    )
                elif 'postal_code' in field:
                    geo_data.update({'postal_code':
                                    geo['lang_address_geocode__postal_code']}
                                    )
                elif 'country' in field:
                    geo_data.update({'country':
                                    geo['lang_address_geocode__country']}
                                    )
                elif 'lat' in field:
                    geo_data.update({'lat': geo['lat']})
                elif 'lng' in field:
                    geo_data.update({'lng': geo['lon']})
            return geo_data
        elif type(output_data) is str:
            address = ''
            address += geo['lang_address_geocode__country'] if \
                geo['lang_address_geocode__country'] and 'country' in fields \
                else ''
            address += ', ' + geo['lang_address_geocode__political_town'] if \
                geo['lang_address_geocode__political_town'] and \
                'political_town' in fields else ''
            address += ', ' + geo['lang_address_geocode__street_title'] if \
                geo['lang_address_geocode__street_title'] and \
                'street_title' in fields else ''
            address += ', ' + geo['lang_address_geocode__street_number'] if \
                geo['lang_address_geocode__street_number'] and \
                'street_number' in fields else ''
            if address[:2] == ', ':
                return address[2:]
            return address
    if type(output_data) is dict:
        return {}
    elif type(output_data) is str:
        return ''
