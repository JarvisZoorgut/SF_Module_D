from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from django_summernote.fields import SummernoteTextField


class Advertisement(models.Model):
    CATEGORIES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = SummernoteTextField(verbose_name='Объявление')
    category = models.CharField(max_length=20, choices=CATEGORIES, verbose_name='Категория')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('advertisement_detail', kwargs={'pk': self.id})

class Response(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='responses', verbose_name='Объявление')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(verbose_name='Отклик')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Отклик на {self.advertisement.title} от {self.user.username}"
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.id})
