from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView
)

from navalny_people.models import Person


class Page404(ListView):

    def get(self, request, *args, **kwargs):
        return render(self.request, '404.html')


class MainPage(ListView):
    """
    Главная страница
    :param request:
    :return:
    """
    model = Person
    active_menu = 'main'
    paginator_class = None
    positions = [1, 2, 1, 3, 1, 2, 1, 3, 1, 2, 1, 3,
                 1, 2, 1, 3, 1, 2, 1, 3, 1, 2, 1, 3, 1]

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
        return render(self.request, 'detail_people_page.html', context=context)


class WriteAboutMe(ListView, CreateView):
    model = Person
    paginator_class = None

    def get(self, request, *args, **kwargs):
        return render(self.request, 'write_about.html')

    def post(self, request, *args, **kwargs):
        user = self.request.user
        about = self.request.POST.get('write', None)
        if about is None:
            return HttpResponseRedirect(
                reverse('404')
            )
        user.bio = about
        user.save(update_fields=['bio'])
        return HttpResponseRedirect(
            reverse('main_page')
        )


class ListPeoplePage(ListView):
    """
    Страница поиска
    :param request:
    :return:
    """
    active_menu = 'people'

    def get(self, request, *args, **kwargs):
        return render(self.request, 'list_people_page.html', {'active': self.active_menu})
