from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.backends import sqlite3
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import sqlite3 as sql
from .forms import UserRegForm, UserLogForm
import yadisk
from .models import Users
from lk.views import photo_to_cloud, try_upload

from django.db.models import F


def reg_log(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/reg_log.html', {'balance': user.Balance})
    return render(request, 'reg_log/reg_log.html')


def valid(user, myuser):
    # if user.id != myuser.id:
    #     return False
    pass


def reg(request):
    error = ''
    if request.user.is_authenticated:
        return redirect('lk')
    if request.method == 'POST':
        form = UserRegForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.FaceLink = user.Face.path[0:62] + 'images/' + user.Face.path[62:].replace(' ', '_')
            # если поменяем путь, надо менять

            user.Balance = 0

            if User.objects.filter(username=user.Email).exists():
                # TODO: сделать нормальную обработку ошибок
                return redirect('home')

            if user.Pass1 != user.Pass2:
                # TODO: сделать нормальную обработку ошибок
                return redirect('reg')

            myuser = User.objects.create_user(username=user.Email, password=user.Pass1)
            myuser.first_name = user.Name
            user.id = myuser.id
            au_user = authenticate(username=user.Email, password=user.Pass1)
            login(request, au_user)
            valid(user, myuser)
            myuser.save()
            user.save()
            return redirect('lk')
        else:
            error = "Форма заполненна неправильно"

    form = UserRegForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'reg_log/reg.html', data)


def log(request):
    error = ''
    if request.user.is_authenticated:
        return redirect('lk')
    if request.method == 'POST':
        form = UserLogForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            au_user = authenticate(username=user.Email, password=user.Pass1)
            if au_user is not None:
                login(request, au_user)
                return redirect('lk')
            else:
                error = "Неверный логин или пароль"
        else:
            error = "Форма заполненна неправильно"

    form = UserLogForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'reg_log/log.html', data)


def out(request):
    logout(request)
    return redirect('home')


def footer(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/footer.html', {'balance': user.Balance})
    return render(request, 'reg_log/footer.html')


def politics(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/politics.html', {'balance': user.Balance})
    return render(request, 'reg_log/politics.html')


def katalog(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/katalog.html', {'balance': user.Balance})
    return render(request, 'reg_log/katalog.html')


def LichnyK(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        return render(request, 'reg_log/lk.html', {'balance': user.Balance})
    return render(request, 'lk/lk.html')


@login_required
def balance(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)
        if request.method == 'POST':
            add_balance = request.POST.get('custom-amount-input')
            user.Balance += int(add_balance)
            user.save()
        return render(request, 'reg_log/balance.html', {'balance': user.Balance})
    return render(request, 'reg_log/balance.html')


@login_required
def profile(request):
    if request.user.is_authenticated:
        user = Users.objects.get(id=request.user.id)

        path = user.FaceLink
        user.FaceLink = photo_to_cloud(path, user.Email)
        if user.FaceLink == 'Error':
            user.delete()
            request.user.delete()
            # надо заново регаться
            # TODO: сделать нормальную обработку ошибок
            return redirect('home')
        else:
            user.save()

        return render(request, 'reg_log/profile.html', {'user': user})
    return render(request, 'reg_log/profile.html')
