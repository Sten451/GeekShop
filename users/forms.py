import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from users.models import User, UserProfile


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Введите имя пользователя"
        self.fields['password'].widget.attrs['placeholder'] = "Введите пароль"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "Введите имя пользователя"
        self.fields['email'].widget.attrs['placeholder'] = "Введите почту"
        self.fields['first_name'].widget.attrs['placeholder'] = "Введите имя"
        self.fields['last_name'].widget.attrs['placeholder'] = "Введите фамилию"
        self.fields['password1'].widget.attrs['placeholder'] = "Введите пароль"
        self.fields['password2'].widget.attrs['placeholder'] = "Подтвердите пароль"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
            
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha256(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha256((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user

    # если вдруг в базе не уникальность
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} уже зарегистрирован на сайте')
        return username

    # если вдруг в базе не уникальность
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с такой почтой {email} уже зарегистрирован на сайте')
        return email


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'first_name', 'last_name', 'image')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    #разобраться
    """def clean_image(self):
        data = self.cleaned_data['image']
        if data.size > 1000000:
            raise forms.ValidationError("Файл слишком большой", code='size')
        return data"""


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tagline', 'about', 'gender', 'language')

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'gender':
                field.widget.attrs['class'] = 'form-control py-4'
            else:
                field.widget.attrs['class'] = 'form-control'
