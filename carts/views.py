from urllib import response
from webbrowser import get
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views import View
from pkg_resources import require
from django.urls import reverse

from carts.mixins import CartMixin
from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products

class CartAddView(CartMixin, View):

    def post(self, request) -> JsonResponse:
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id = product_id)

        cart = self.get_cart(request, product = product)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user = request.user if request.user.is_authenticated else None,
                                session_key = request.session.session_key if not request.user.is_authenticated else None,
                                product = product, quantity = 1)
            
        response_data = {
            'message': 'Товар добавлен в корзину',
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)
    
class CartChangeView(CartMixin, View):

    def post(self, request):
        cart_id = request.POST.get('cart_id')

        cart = self.get_cart(request, cart_id = cart_id)

        cart.quantity = request.POST.get('quantity')
        cart.save()

        quantity = cart.quantity

        response_data = {
            'message': 'Количество изменено',
            'quantity': quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)
    
class CartRemoveView(CartMixin, View):

    def post(self, request):
        cart_id = request.POST.get('cart_id')

        cart = self.get_cart(request, cart_id = cart_id)
        quantity = cart.quantity

        cart.delete()

        response_data = {
            'message': 'Товар удалён',
            'quantity_deleted': quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)

# def cart_add(request) -> JsonResponse:

#     product_id = request.POST.get("product_id")
    
#     product = Products.objects.get(id = product_id)

#     if request.user.is_authenticated:
#         carts = Cart.objects.filter(user = request.user, product = product)

#         if carts.exists():
#             cart = carts.first()
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
#         else:
#             Cart.objects.create(user = request.user, product = product, quantity = 1)
    
#     else:
#         carts = Cart.objects.filter(
#             session_key = request.session.session_key, product = product)
        
#         if carts.exists():
#             cart = carts.first()
#             if cart:
#                 cart.quantity += 1
#                 cart.save()
        
#         else:
#             Cart.objects.create(
#                 session_key = request.session.session_key, product = product, quantity = 1)

#     user_cart = get_user_carts(request)
#     cart_items_html = render_to_string(
#         "carts/includes/included_cart.html", {"carts": user_cart}, request = request)

#     response_data = {
#         "message": "Товар добавлен в корзину",
#         "cart_items_html": cart_items_html,
#     }

#     return JsonResponse(response_data)


# def cart_change(request) -> JsonResponse:
    
#     cart_id = request.POST.get("cart_id")
#     quantity = request.POST.get("quantity")

#     cart = Cart.objects.get(id = cart_id)

#     cart.quantity = quantity
#     cart.save()
#     updated_quantity = cart.quantity

#     # cart = get_user_carts(request)

#     user_cart = get_user_carts(request)
#     context = {"carts": user_cart}

#     referer = request.META.get('HTTP_REFERER')
#     if reverse('orders:create_order') in referer:
#         context["orders"] = True

#     cart_items_html = render_to_string(
#         "carts/includes/included_cart.html", context, request = request)
    
#     response_data = {
#         "message": "Количество изменено",
#         "cart_items_html": cart_items_html,
#         "quantity": updated_quantity,
#     }

#     return JsonResponse(response_data)

# def cart_remove(request) -> JsonResponse:
    
#     cart_id = request.POST.get("cart_id")

#     cart = Cart.objects.get(id = cart_id)
#     quantity = cart.quantity
#     cart.delete()

#     user_cart = get_user_carts(request)

#     context = {"carts": user_cart}

#     referer = request.META.get('HTTP_REFERER')
#     if reverse('orders:create_order') in referer:
#         context["orders"] = True

#     cart_item_html = render_to_string(
#         "carts/includes/included_cart.html", context, request = request)
    
#     response_data = {
#         "message": "Товар удалён",
#         "cart_item_html": cart_item_html,
#         "quantity_deleted": quantity,
#     }

#     return JsonResponse(response_data)