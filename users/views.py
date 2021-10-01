from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from baskets.models import Basket
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались.")
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные сохранены")
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            if 'image' in form.errors:
                dict2 = (form.errors.get_json_data()).get('image')
                if (dict2[-1]['code']) == 'size':
                    messages.error(request, "Размер картинки должен быть меньше 1МБ")
                elif (dict2[-1]['code']) == 'invalid_image':
                    messages.error(request, "Файл, который Вы загрузили, повреждён или не является изображением")
            else:
                messages.error(request, "Неизвестная ошибка сохранения данных")

    total_sum = 0
    total_quantity = 0
    baskets = Basket.objects.filter(user=request.user)
    for s in baskets:
        total_quantity += s.quantity
        total_sum += s.sum()

    context = {
        'title': 'Профайл',
        'form': UserProfileForm(instance=request.user),
        'baskets': Basket.objects.filter(user=request.user),
        'total_sum': total_sum,
        'total_quantity': total_quantity

    }
    return render(request, 'users/profile.html', context)
