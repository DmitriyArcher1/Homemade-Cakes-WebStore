from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.core.cache import cache

from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('main:index') # формирует строку маршрута, когда пользователь её уже запросит

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page

        return reverse_lazy('main:index')
    
    def form_valid(self, form) -> HttpResponseRedirect | None:
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                # удаляем старые корзины
                forgot_carts = Cart.objects.filter(user = user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                
                # добавляем авторизованному пользователю корзину из анонимной сессии
                Cart.objects.filter(session_key = session_key).update(user = user)

                messages.success(self.request, f'{user.username}, Вы вошли в систему.')

                return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HC - Авторизация'

        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form) -> HttpResponseRedirect:
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key = session_key).update(user = user)
            
        messages.success(self.request, f'{user.username}, Вы успешно зарегистрировались и вошли в аккаунт')
        return HttpResponseRedirect(self.success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HC - Регистрация'

        return context


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView): # LoginRequiredMixin проверяет, авторизован ли пользователь
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset = None):
        return self.request.user
    
    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, f'Профиль успешно обновлён')
        return super().form_valid(form)
    
    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, f'Произошла ошибка')
        return super().form_invalid(form) 
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HC - Личный кабинет'

        orders = Order.objects.filter(user = self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset = OrderItem.objects.select_related("product"),
            )
        ).order_by("-id")
        
        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}", 60 * 2)
        return context
    
class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HC - Корзина'

        return context

@login_required
def logout(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    messages.success(request, f"{request.user.username}, Вы вышли из системы")
    auth.logout(request)
    return redirect(reverse('main:index'))
    


# def users_cart(request) -> HttpResponse:
#     return render(request, 'users/users_cart.html')


# @login_required
# def profile(request) -> HttpResponseRedirect | HttpResponse:

#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES) # передаём данные из словаря, которые указал пользователь
 
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Профиль успешно обновлён.")
#             return HttpResponseRedirect(reverse('users:profile'))
    
#     else:
#         form = ProfileForm(instance=request.user)

#     orders = (
#         Order.objects.filter(user = request.user)
#             .prefetch_related(
#                 Prefetch(
#                     "orderitem_set",
#                     queryset = OrderItem.objects.select_related('product')
#                 )
#             )
#         .order_by('-id')
#     )

#     context = {
#         'title': 'HC - Личный кабинет',
#         'form': form,
#         'orders': orders,
#     }

#     return render(request, 'users/profile.html', context)


# def login(request) -> HttpResponseRedirect | HttpResponse:
    
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST) # передаём словарь с данными

#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             # проверка на то, есть ли уже такой пользователь или нет

#             session_key = request.session.session_key

#             # если возвращается объект user(он есть в БД)
#             if user:
#                 auth.login(request, user) # то авторизуем его
#                 messages.success(request, f"{username}, Вы вошли в систему.")

#                 if session_key:
#                     # Удаление старых корзин авторизованных пользователей
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()

#                     # добавление новых корзин авторизованных пользователей из анонимной сессии               
#                 Cart.objects.filter(session_key = session_key).update(user = user)

#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('users:logout'):
#                     return HttpResponseRedirect(request.POST.get('next'))
                
#                 return HttpResponseRedirect(reverse('main:index')) # перенаправляем на главную страницу
    
#     else:
#         form = UserLoginForm()
            
#     context = {
#         'title': 'HC - Авторизация',
#         'form': form,
#     }

#     return render(request, 'users/login.html', context)


# def registration(request) -> HttpResponseRedirect | HttpResponse:

#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST) # передаём данные из словаря, которые указал пользователь
 
#         if form.is_valid():
#             form.save()

#             session_key = request.session.session_key

#             user = form.instance
#             auth.login(request, user)

#             if session_key:
#                 Cart.objects.filter(session_key = session_key).update(user = user)
            
#             messages.success(request, f"{user.username}, Вы успешно зарегистрировались и вошли в систему.")
#             return HttpResponseRedirect(reverse('main:index')) # и перенаправляем на страницу с авторизацией
    
#     else:
#         form = UserRegistrationForm()

#     context = {
#         'title': 'HC - Регистрация',
#         'form': form,
#     }

#     return render(request, 'users/registration.html', context)
