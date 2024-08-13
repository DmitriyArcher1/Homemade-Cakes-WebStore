from django.contrib.auth.decorators import login_required
import re
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from users.models import User


def login(request):
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST) # передаём словарь с данными

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            # проверка на то, есть ли уже такой пользователь или нет

            # если возвращается объект user(он есть в БД)
            if user:
                auth.login(request, user) # то авторизуем его
                messages.success(request, f"{username}, Вы вошли в свой аккаунт.")
                return HttpResponseRedirect(reverse('main:index')) # и перенаправляем на главную страницу
    
    else:
        form = UserLoginForm()
            
    context = {
        'title': 'HC - Авторизация',
        'form': form,
    }

    return render(request, 'users/login.html', context)

def registration(request):

    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST) # передаём данные из словаря, которые указал пользователь
 
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрировались и вошли в свой аккаунт.")
            return HttpResponseRedirect(reverse('main:index')) # и перенаправляем на страницу с авторизацией
    
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'HC - Регистрация',
        'form': form,
    }

    return render(request, 'users/registration.html', context)

@login_required
def profile(request):

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

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта.")
    auth.logout(request)
    return redirect(reverse('main:index'))