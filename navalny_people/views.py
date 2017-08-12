from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView, CreateView
)

from navalny_people.models import Person


def page_not_found(request):
    return render(request, '404.html')


class Page404(ListView):
    def get(self, request, *args, **kwargs):
        return render(self.request, '404.html')


class RandomPersons(ListView):
    model = Person

    def get(self, request, *args, **kwargs):
        counts = self.request.GET.get('count', 2)
        excluded_persons = self.request.GET.get('exclude')
        persons = self.model.objects.order_by('?').exclude(pk__in=[
            x for x in excluded_persons.split(',')
        ])[:counts]
        context = {'persons': map(lambda x: {
            'id': x.pk, 'first_name': x.first_name,
            'last_name': x.last_name},
            persons)}
        return JsonResponse(context)


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
            return HttpResponseRedirect(
                reverse('404')
            )
        person = self.get_queryset().get(pk=person_id)
        context = {
            'person': person
        }
        return render(self.request, 'detail_people_page.html', context=context)


class WriteAboutMe(ListView, CreateView):
    model = Person
    paginator_class = None

    def get(self, request, *args, **kwargs):
        return render(self.request, 'write_form_page.html')

    def post(self, request, *args, **kwargs):
        context = {}
        for key, value in self.request.POST.items():
            if key != '' or value is not None:
                if key in 'region':
                    context[key] = value
                elif key in 'first_name':
                    context[key] = value
                elif key in 'second_name':
                    context[key] = value
                elif key in 'profession':
                    context[key] = value
                elif key in 'donations':
                    context[key] = value
                elif key in 'email':
                    context[key] = value
                elif key in 'story':
                    context[key] = value
        print(context)
        # person = self.model.objects.create(**context)
        # TODO: Stmh with person object
        if len(context.keys()) == 0:
            return HttpResponseRedirect(
                reverse('404')
            )
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
