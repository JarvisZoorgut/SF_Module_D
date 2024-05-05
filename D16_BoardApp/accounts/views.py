from .models import CustomUser
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.shortcuts import render
from .forms import SignUpForm


class SignUp(CreateView):
    model = CustomUser
    form_class = SignUpForm
    success_url = '/accounts/confirm_registration/'
    template_name = 'accounts/templates/registration/signup.html'


class ConfirmRegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/templates/registration/confirm_registration.html', {})

    def post(self, request, *args, **kwargs):
        confirmation_code = request.POST.get('confirmation_code')
        email = request.POST.get('email')  # Получаем введенный email
        
        # Проверяем, что оба поля не пустые
        if not confirmation_code or not email:
            return render(request, 'accounts/templates/registration/conf_error.html', {'error_message': 'Введите код подтверждения и email'})

        user = CustomUser.objects.filter(email=email, confirmation_code=confirmation_code).first()
        if user:
            # Подтверждение регистрации пользователя
            user.is_active = True
            user.confirmation_code = ''  # Очистка кода подтверждения
            user.save()
            return render(request, 'accounts/templates/registration/reg_conf.html', {})  # Перенаправление на страницу с подтверждением
        else:
            # Обработка неправильного кода подтверждения или email
            return render(request, 'accounts/templates/registration/conf_error.html', {'error_message': 'Неправильный код подтверждения или email'})