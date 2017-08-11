from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView
)

from navalny_people.models import Person


class MainPage(ListView):
    """
    Главная страница
    :param request:
    :return:
    """
    model = Person
    positions = [1, 2, 1, 3, 1, 2, 1, 3, 1, 2, 1, 3,
                 1, 2, 1, 3, 1, 2, 1, 3, 1, 2, 1, 3, 1]
    paginator_class = None

    active_menu = 'main'

    def get_queryset(self):
        return self.model.objects. \
            select_related('address').order_by('?')[:25]

    def get(self, request, *args, **kwargs):
        persons = self.get_queryset()
        for i, person in enumerate(persons):
            person.position = self.positions[i]
        context = {
            'persons': persons,
            'active': self.active_menu
        }
        return render(self.request, 'main_page.html', context=context)


class AboutPage(ListView):
    """
    Страница "О нас"
    :param request:
    :return:
    """

    def get(self, request, *args, **kwargs):
        return render(self.request, 'example.html')


class ListProfilesPage(ListView):
    """
    Страница профилей
    :param request:
    :return:
    """
    model = Person
    paginator_class = None

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        limit = self.request.GET.get('limit', 10)
        offset = self.request.GET.get('offset', 0)
        persons = self.get_queryset()[offset:offset + limit]
        context = {
            'persons': persons
        }
        return render(self.request, 'example.html', context=context)


class DetailProfilePage(DetailView):
    """
    Страница профиля
    :param request:
    :return:
    """
    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        person_id = kwargs['pk']
        if not self.queryset.filter(pk=person_id).exists():
            return render(self.request, '404.html')
        person = self.get_queryset().get(pk=person_id)
        context = {
            'person': person
        }
        return render(self.request, 'example.html', context=context)


class PeoplePage(ListView):
    """
    Страница поиска
    :param request:
    :return:
    """
    active_menu = 'people'

    def get(self, request, *args, **kwargs):
        return render(self.request, 'people_page.html', {'active': self.active_menu})
