from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from goods.models import Products


def catalog(request, category_slug, page=1):

    if category_slug == "all":
        goods = Products.objects.all() # получение всех товаров из базы данных
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug)) 
        # иначе получаем товары по определенной категории
    
    paginator = Paginator(goods, 3)
    current_page = paginator.page(page)

    context = {
        "title": "HC - Каталог",
        "goods": current_page,
        "slug_url": category_slug,
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    
    product = Products.objects.get(slug = product_slug)

    context = {
        'product': product,
    }

    return render(request, "goods/product.html", context = context)