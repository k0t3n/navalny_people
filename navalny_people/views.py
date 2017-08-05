from django.shortcuts import render, HttpResponse


def example(request):
    return render(request, 'example.html')
