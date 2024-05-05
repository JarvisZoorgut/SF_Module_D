from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput, help_text=("<p>Ваш пароль не должен быть слишком простым. Он должен содержать как минимум 8 символов и не должен состоять только из цифр."))


    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        CustomUser = super().save(commit=False)
        if commit:
            confirmation_code = get_random_string(length=6)  # Генерация уникального кода
            CustomUser.confirmation_code = confirmation_code  # Сохранение кода в модели пользователя
            CustomUser.is_active = False
            CustomUser.save()
            subject = 'Добро пожаловать на наш сайт!'
            html_message = render_to_string('accounts/templates/registration/registration_email.html', {'user': CustomUser, 'code': confirmation_code})
            
            msg = EmailMultiAlternatives(subject=subject, body=html_message, from_email=None, to=[CustomUser.email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
        return CustomUser

