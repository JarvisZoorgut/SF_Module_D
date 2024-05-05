from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Response


@receiver(post_save, sender=Response)
def send_notification_email(sender, instance, created, **kwargs):
    # Проверяем, если отзыв создан на объявление и это создание нового объекта
    if created and instance.advertisement:
        # Получаем адрес электронной почты создателя объявления
        recipient_email = instance.advertisement.creator.email
        # Отправляем сообщение
        subject = f'Новый отклик на ваше объявление {instance.advertisement.title}'

        text_content = (
            f'Отклик: {instance.content}\n\n'
            f'Все отклики на ваше объявление: http://127.0.0.1:8000/private-responses/'
        )
        html_content = (
            f'<p>Отклик: {instance.content}</p><br>'
            f'<p><a href="http://127.0.0.1:8000/board/private-responses/">Все отклики на ваше объявление</a></p>'
        )
        msg = EmailMultiAlternatives(subject, text_content, None, [recipient_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@receiver(post_save, sender=Response)
def send_acceptance_notification(sender, instance, created, **kwargs):
    # Проверяем, если отклик был принят
    if instance.accepted:
        # Получаем адрес электронной почты отправителя отклика
        sender_email = instance.user.email
        # Отправляем сообщение
        subject = 'Ваш отклик был принят'
        text_content = f'Ваш отклик "{instance.content[:10]}..." на объявление "{instance.advertisement.title}" был принят.'
        html_content = f'<p>Ваш отклик "{instance.content[:10]}..." на объявление "{instance.advertisement.title}" был принят.</p>'
        msg = EmailMultiAlternatives(subject, text_content, None, [sender_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()