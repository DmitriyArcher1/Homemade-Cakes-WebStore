import re
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm
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
            return HttpResponseRedirect(reverse('main:index')) # и перенаправляем на страницу с авторизацией
    
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'HC - Регистрация',
        'form': form,
    }

    return render(request, 'users/registration.html', context)


def profile(request):
    context = {
        'title': 'HC - Личный кабинет'
    }

    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))