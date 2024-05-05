import logging
from collections import defaultdict

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from board.models import Advertisement

logger = logging.getLogger(__name__)


def send_weekly_advertisements():
    advertisements = Advertisement.objects.all()

    # Создаем словарь для хранения уникальных адресов электронной почты авторов объявлений
    email_dict = defaultdict(list)

    for advertisement in advertisements:
        # Определяем, было ли уже выполнение задачи
        last_execution = DjangoJobExecution.objects.filter(
            job_id="send_weekly_advertisements", status=DjangoJobExecution.SUCCESS
        ).order_by("-run_time").first()

        # Если было, берем время последнего выполнения
        if last_execution:
            last_execution_time = last_execution.run_time
        else:
            # Если нет, берем время, равное текущему времени минус 7 дней
            last_execution_time = timezone.now() - timezone.timedelta(days=7)

        # Фильтруем объявления, опубликованные после последнего выполнения
        new_advertisements = Advertisement.objects.filter(
            created_at__gt=last_execution_time
        )

        for ad in new_advertisements:
            # Добавляем адрес электронной почты автора в словарь, если он еще не там
            email_dict[ad.creator.email].append(ad)

    # Отправляем письма авторам объявлений
    for email, ads in email_dict.items():
        subject = f'Еженедельное обновление: Новые объявления'
        text_content = "Новые объявления:\n\n"
        html_content = "Новые объявления:<br><br>"
        for ad in ads:
            text_content += f'{ad.title} - {ad.content[:20]}...\n'
            html_content += f'<a href="http://127.0.0.1:8000{ad.get_absolute_url()}">{ad.title}</a> - {ad.content[:20]}...<br>'
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    logger.info("Weekly advertisements sent successfully!")


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=timezone.get_current_timezone())
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_advertisements,
            trigger=CronTrigger(day_of_week="wed", hour="18", minute="25"),
            id="send_weekly_advertisements",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_advertisements'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="sun", hour="0", minute="0"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
