from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories


# создание контролера (тоже самое, что и функция, но в джанго говорят именно так)
# в параметр request попадает экземпляр класса http request, который содержит все данные о запросе пользователя
class IndexView(TemplateView):
    template_name = 'main/index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HC - Главная'
        context['content_title'] = ''
        context['content_text'] = ''

        return context
    
class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HC - О нас'
        context['content'] = 'Краткая информация про нас'
        context['text_on_page'] = 'Наш магазин изготавливает торты по домашнему рецепту под заказ.'

        return context

# def index(request):


#     context = {
#         'title': 'HC - Главная',
#         'content_title': 'HOMEMADE CAKES',
#         'content_text': 'Магазин домашних тортов',
#     }

#     return render(request, 'main/index.html', context)


# def about(request):
#     context = {
#         'title': 'HC - О нас',
#         'content': 'Краткая информация про нас',
#         'text_on_page': 'Наш магазин изготавливает торты по домашнему рецепту под заказ.'
#     }

#     return render(request, 'main/about.html', context)