from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives, mail_managers
from allauth.account.forms import SignupForm
from django.template.loader import render_to_string


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name="authors")
        user.groups.add(authors)

        subject = 'Добро пожаловать в наш интернет-магазин!'
        html_message = render_to_string('accounts/templates/registration/registration_email.html', {'user': user})
        
        msg = EmailMultiAlternatives(subject=subject, body=html_message, from_email=None, to=[user.email])
        msg.attach_alternative(html_message, "text/html")
        msg.send()

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user
