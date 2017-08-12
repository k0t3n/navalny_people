import json
import os
import urllib
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
    filename = '%s.%s' % (uuid.uuid4(), ext)
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
        filter(**{'user_location': pk}). \
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


def fetch_social_data(social_id, social_type, token=None):
    """
    Fetch account data from social networks
    :param social_id: ID account fetched from SocNetworks
    :param token: optional param for send token
    :param social_type: type{VK/FB}
    :return: tuple with data
    """
    null = None
    SocialAccount = namedtuple('SocialAccount', [
        'first_name', 'last_name', 'email', 'birthday', 'avatar', 'uid'])
    user_model = __import__('navalny_people.models', globals(), locals(),
                            ['Person'], -1)
    social_type = int(social_type)
    if social_type == user_model.User.VK:
        vk_user_url = 'https://api.vk.com/method/users.get?uids=%s&' \
                      'fields=uid,first_name,last_name,bdate,' \
                      'photo_100' % social_id
        vk_data_url = urllib.request.urlopen(vk_user_url)
        vk_dump = json.load(vk_data_url)
        SocialAccount.email = null
        SocialAccount.uid = vk_dump['response'][0].get('uid', null)
        SocialAccount.first_name = vk_dump['response'][0].get('first_name',null)
        SocialAccount.last_name = vk_dump['response'][0].get('last_name', null)
        if 'bdate' in vk_dump['response'][0]:
            bdate = vk_dump['response'][0].get('bdate', null)
            tmp_birthday = None
            if len(bdate) > 5 and bdate != null:
                SocialAccount.birthday = datetime. \
                    strptime(bdate, '%d.%m.%Y').strftime('%Y-%m-%d')
            else:
                SocialAccount.birthday = datetime. \
                    strptime(bdate, '%d.%m').strftime('1970-%m-%d')
        SocialAccount.avatar = vk_dump['response'][0]['photo_200']

        return SocialAccount
    elif social_type == user_model.User.FB:
        fb_user_url = 'https://graph.facebook.com/v2.8/%s?fields=id,' \
                      'birthday,first_name,last_name,email,' \
                      'picture&locale=ru&access_token=%s' % (social_id, token)
        fb_data_url = urllib.request.urlopen(fb_user_url)
        fb_pic_url = 'https://graph.facebook.com/v2.8/%s/picture?' \
                     'width=200&height=200' % social_id
        SocialAccount.avatar = urllib.request.urlopen(fb_pic_url).url
        fb_dump = json.load(fb_data_url)
        SocialAccount.uid = fb_dump.get('uid', null)
        SocialAccount.email = fb_dump.get('email', null)
        SocialAccount.last_name = fb_dump.get('last_name', null)
        SocialAccount.first_name = fb_dump.get('first_name', null)
        if 'birthday' in fb_dump:
            bdate = fb_dump['birthday']
            SocialAccount.birthday = datetime. \
                strptime(bdate, '%m/%d/%Y').strftime('%Y-%m-%d')

        return SocialAccount
    else:
        return null
