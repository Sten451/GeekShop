from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, reverse, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView
from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User

class Logout(LogoutView):
    template_name = 'mainapp/index.html'

class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'

class RegisterListView(FormView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    not_success_url = reverse_lazy('users:register')
    title = 'Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verification(user):
                messages.success(request, "Письмо с кодом активации направлено на Ваш почтовый адрес.")
            return redirect(self.success_url)
        else:
            messages.error(request,"Ошибка регистрации, попробуйте другой НИК или почту")
            return redirect(self.not_success_url)


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Профайл'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST,files=request.FILES,instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)


def verify(request, email, activation_key):
    user = User.objects.get(email=email)
    if user and user.activation_key == activation_key and not user.is_activation_key_expired():
        user.activation_key = ''
        user.activation_key_created = None
        user.is_active = True
        user.save()
        auth.login(request, user)
    return render(request, 'users/verification.html')


def send_verification(user):
    verify_link = reverse('users:verify', args=[user.email,user.activation_key])
    subject = f'Для активации учётной записи {user.username} пройдите по ссылке'
    message = f'Для подтверждения учётной записи {user.username} на сайте \n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email],fail_silently=False)

