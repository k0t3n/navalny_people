from django.conf.urls import url, include
from navalny_people.views import (
    MainPage, AboutPage, ListPeoplePage,
    WriteAboutMe, DetailProfilePage,
    RandomPersons, Login)


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
        r'^refresh/$',
        RandomPersons.as_view(),
        name='refresh_persons'
    ),
    url(
        r'^people/$',
        ListPeoplePage.as_view(),
        name='people_page'
    ),
    url(
        r'^write/$',
        WriteAboutMe.as_view(),
        name='write_page'
    ),
    url(
        r'^person/', include([
            # url(
            #     r'^$',
            #     # TODO: шо тута???
            #     name='list_persons'
            # ),
            url(
                r'^(?P<pk>\d+)/$',
                DetailProfilePage.as_view(),
                name='detail_person'
            )
        ])
    ),
    url(
        r'^login/$',
        Login.as_view(),
        name='login'
    ),
]
