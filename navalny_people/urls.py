from django.conf.urls import url, include
from navalny_people.views import (
    AboutPage, PeoplePage, DetailProfilePage, MainPage,
    ListProfilesPage
)

urlpatterns = [
    url(
        r'^$',
        MainPage.as_view(),
        name='main_page'
    ),
    url(
        r'^about/$',
        AboutPage.as_view(),
        name='about_page'
    ),
    url(
        r'^people/$',
        PeoplePage.as_view(),
        name='people_page'
    ),
    url(
        r'^person/', include([
            url(
                r'^$',
                ListProfilesPage.as_view(),
                name='list_persons'
            ),
            url(
                r'^(?P<pk>\d+)/$',
                DetailProfilePage.as_view(),
                name='detail_person'
            )
        ])
    )
]
