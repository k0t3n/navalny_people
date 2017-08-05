from django.shortcuts import render, HttpResponse


def example(request):
    return render(request, 'example.html')


def main_page(request):
    """
    Главная страница
    :param request:
    :return:
    """
    return HttpResponse('not ready yet')


def about_page(request):
    """
    Страница "О нас"
    :param request:
    :return:
    """
    return HttpResponse('not ready yet')


def profile_page(request):
    """
    Страница профиля
    :param request:
    :return:
    """
    return HttpResponse('not ready yet')


def search_page(request):
    """
    Страница поиска
    :param request:
    :return:
    """
    return HttpResponse('not ready yet')