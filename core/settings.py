import os
from core.settings_local import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-)agk^!pxbcf9&krm@rr&)=&%0sh0rst!b5$fwvbkpt0w_+p3-'
AUTH_USER_MODEL = 'navalny_people.Person'
INSTALLED_APPS = [
    # Admin apps
    'suit',
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Project_apps
    'geodata',
    'navalny_people',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'core.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]
WSGI_APPLICATION = 'core.wsgi.application'
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
MEDIA_URL = '/files/'
STATIC_ROOT = os.path.join(BASE_DIR, 'navalny_people/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


GOOGLEMAPS_KEY = 'AIzaSyCi3dmQDG8mz6Mb6w1FzVXk-OvYfUvZE04'
VK_CLIENT_ID = '6093659'
VK_SECRET_KEY = 'kTJuqF3GBO7UGtL4NlDJ'
FACEBOOK_CLIENT_ID = '1581457421898430'
FACEBOOK_SECRET_KEY = 'bae43ff92729c0674f317d3a3d5154fd'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Навальный.Люди',
    'MENU_EXCLUDE': ('auth.group', 'auth'),
}

