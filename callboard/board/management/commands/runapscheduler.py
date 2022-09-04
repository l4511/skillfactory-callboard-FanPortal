import logging
import datetime
from django.conf import settings
from board.models import Notice, User
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def my_job():
    delta = datetime.timedelta(1)
    start_date = datetime.datetime.utcnow() - delta
    end_date = datetime.datetime.utcnow()
    notice_for_day_send = Notice.objects.filter(notice_time_create__range=(start_date, end_date))
    html_content = render_to_string('email/send.html', {'notices': notice_for_day_send}, )
    email = set()
    for user in User.objects.all():
        email.add(User.objects.filter(username=user).values("email")[0]['email'])
    msg = EmailMultiAlternatives(
        subject=f'"У нас новые объявления сегодня!"',
        body='',
        from_email='alexgoldm1991@yandex.ru',
        to=email
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/1"),
            # То же, что и интервал, но задача триггера таким образом более понятна django
            id="my_job",  # уникальный ID
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи,
            # которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
