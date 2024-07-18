from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


# создание контролера (тоже самое, что и функция, но в джанго говорят именно так)
# в параметр request попадает экземпляр класса http request, который содержит все данные о запросе пользователя
def index(request):


    context = {
        'title': 'HC - Главная',
        'content_title': 'HOMEMADE CAKES',
        'content_text': 'Магазин домашних тортов',
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'HC - О нас',
        'content': 'Краткая информация про нас',
        'text_on_page': 'Наш магазин изготавливает торты по домашнему рецепту под заказ.'
    }

    return render(request, 'main/about.html', context)