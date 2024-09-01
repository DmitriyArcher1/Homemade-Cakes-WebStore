from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

@login_required
def create_order(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:

    if request.method == 'POST':
        form = CreateOrderForm(data = request.POST)
        if form.is_valid():

            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user = user)

                    if cart_items.exists():
                        # Создаём заказ, если есть товары в корзине
                        order = Order.objects.create(
                            user = user,
                            phone_number = form.cleaned_data['phone_number'], # из словаря по ключу получаем значение
                            requires_delivery = form.cleaned_data['requires_delivery'],
                            delivery_address = form.cleaned_data['delivery_address'],
                            payment_on_get = form.cleaned_data['payment_on_get'],
                        )

                        # Создаём заказанные товары
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f"Недостаточное количество товара {name} на складе\
                                                      В наличии - {product.quantity}")
                            
                            OrderItem.objects.create(
                                order = order,
                                product = product,
                                name = name,
                                price = price,
                                quantity = quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        # Очищаем корзину пользователя после создания заказа
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')
                        return redirect('users:profile')
                        
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('carts:order')
            
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = CreateOrderForm(initial = initial)
    
    context = {
        'title': 'HC - Оформление заказа',
        'form': form,
        'order': True,
    }

    return render(request, 'orders/create_order.html', context = context)