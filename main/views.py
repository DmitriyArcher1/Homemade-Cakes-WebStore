from django.http import HttpResponse
from django.shortcuts import render


# создание контролера (тоже самое, что и функция, но в джанго говорят именно так)
# в параметр request попадает экземпляр класса http request, который содержит все данные о запросе пользователя
def index(request):
    context = {
        'title': 'Главная',
        'content': 'Главная страница магазина - Домашние торты',
        'list': ['first', 'second'],
        'dict': {'first': 1},
        'is_authenticated': False
    }

    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse('About page')