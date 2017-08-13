from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from navalny_people.views import Page404

urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^',
        include('navalny_people.urls')
    ),
    url(
        r'^404/$',
        Page404.as_view(),
        name='404'
    )
]

handler404 = 'navalny_people.views.page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
