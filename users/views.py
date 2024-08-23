from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from carts.models import Cart
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from users.models import User


def login(request) -> HttpResponseRedirect | HttpResponse:
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST) # передаём словарь с данными

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            # проверка на то, есть ли уже такой пользователь или нет

            session_key = request.session.session_key

            # если возвращается объект user(он есть в БД)
            if user:
                auth.login(request, user) # то авторизуем его
                messages.success(request, f"{username}, Вы вошли в систему.")

                if session_key:
                    Cart.objects.filter(session_key = session_key).update(user = user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('users:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse('main:index')) # перенаправляем на главную страницу
    
    else:
        form = UserLoginForm()
            
    context = {
        'title': 'HC - Авторизация',
        'form': form,
    }

    return render(request, 'users/login.html', context)

def registration(request) -> HttpResponseRedirect | HttpResponse:

    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST) # передаём данные из словаря, которые указал пользователь
 
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key = session_key).update(user = user)
            
            messages.success(request, f"{user.username}, Вы успешно зарегистрировались и вошли в систему.")
            return HttpResponseRedirect(reverse('main:index')) # и перенаправляем на страницу с авторизацией
    
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'HC - Регистрация',
        'form': form,
    }

    return render(request, 'users/registration.html', context)

@login_required
def profile(request) -> HttpResponseRedirect | HttpResponse:

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES) # передаём данные из словаря, которые указал пользователь
 
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён.")
            return HttpResponseRedirect(reverse('users:profile'))
    
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': 'HC - Личный кабинет',
        'form': form,
    }

    return render(request, 'users/profile.html', context)


def users_cart(request) -> HttpResponse:
    return render(request, 'users/users_cart.html')


@login_required
def logout(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    messages.success(request, f"{request.user.username}, Вы вышли из системы")
    auth.logout(request)
    return redirect(reverse('main:index'))