from django.conf.urls import url
from navalny_people import views

urlpatterns = [
    url(r'^$', views.example),
    # TODO /person/{number}
    # TODO /about
    # TODO /search
]
