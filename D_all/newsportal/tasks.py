from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import datetime

from .models import Post
from django.contrib.auth.models import User


@shared_task
def send_notification_email(preview, post_id, title, subscribers):
    # Преобразуем ManyRelatedManager в список объектов подписчиков
    if hasattr(subscribers, 'all'):
        subscribers = subscribers.all()

    # Извлекаем адреса электронной почты из объектов подписчиков
    email_list = [subscriber.user.email for subscriber in subscribers]

    html_content = render_to_string(
        "newsportal/post_created_email.html",
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{post_id}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email_list,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('AddNewPost notify message sent')


@shared_task
def notify_subscribers_about_weekly_news():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(User.objects.filter(subscribers__category__name__in=categories).values_list('email', flat=True))
    html_content = render_to_string(
        'newsportal/daily_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('Weekly notify message send')
