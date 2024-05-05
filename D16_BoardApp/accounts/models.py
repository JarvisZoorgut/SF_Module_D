from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'