from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from goods.models import Products


def catalog(request, category_slug):

    page = request.GET.get("page", 1) # GET - словарь, а get - уже метод, применяемыый к этому словарю
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)


    if category_slug == "all":
        goods = Products.objects.all() # получение всех товаров из базы данных
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug)) 
        # иначе получаем товары по определенной категории
    
    if on_sale:
        goods = goods.filter(dicsount__gt=0) # скидки больше, чем 0
    
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)
    
    # пагинация
    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

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