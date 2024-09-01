from carts.models import Cart

def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user = request.user).select_related('product') # выбираем корзины данного пользователя и отображаем их
    
    if not request.session.session_key:
        request.session.create()
    
    return Cart.objects.filter(session_key = request.session.session_key).select_related('product')

# select_related означает то, что выполнятеся лишь один SQL запрос модели product и cart